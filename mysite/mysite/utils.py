import numpy as np
from PIL import Image
import io
import os
import sys

# 延迟导入onnxruntime，避免在模块加载时就尝试加载模型
rt = None

# 模型路径
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resnet50_garbage_final.onnx')
print(f"模型路径: {model_path}", file=sys.stderr)

# 垃圾类别映射 - 根据用户提供的信息更新为3类
class_names = [
    "纸张",
    "玻璃", 
    "塑料"
]

def get_model_session():
    """
    懒加载模型会话
    
    返回:
        模型会话对象或None
    """
    global rt
    
    # 动态导入onnxruntime
    if rt is None:
        try:
            import onnxruntime
            rt = onnxruntime  # 更新全局变量
            print(f"成功导入onnxruntime，版本: {rt.__version__}", file=sys.stderr)
        except ImportError as e:
            error_msg = f"无法导入onnxruntime: {e}"
            print(error_msg, file=sys.stderr)
            return None
    
    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        error_msg = f"模型文件不存在: {model_path}"
        print(error_msg, file=sys.stderr)
        return None
    else:
        print(f"模型文件存在，大小: {os.path.getsize(model_path)} 字节", file=sys.stderr)
    
    try:
        # 尝试创建推理会话，添加更多的错误捕获
        print(f"正在创建模型会话...", file=sys.stderr)
        session = rt.InferenceSession(model_path)
        print(f"模型会话创建成功，输入名称: {[input.name for input in session.get_inputs()]}", file=sys.stderr)
        print(f"模型会话创建成功，输出名称: {[output.name for output in session.get_outputs()]}", file=sys.stderr)
        return session
    except Exception as e:
        error_msg = f"加载模型失败: {e}"
        print(error_msg, file=sys.stderr)
        return None

def model_predict(image_array):
    """
    使用ONNX模型进行实际预测
    
    参数:
        image_array: 预处理后的图像数组
    
    返回:
        预测的类别名称和置信度
    """
    try:
        # 获取模型会话（懒加载）
        session = get_model_session()
        
        # 如果模型未加载成功，返回默认值
        if session is None:
            print("模型会话为None，无法进行预测", file=sys.stderr)
            return "模型加载失败", 0.0
        
        # 获取实际的输入名称
        try:
            input_name = session.get_inputs()[0].name
            print(f"使用实际输入名称: {input_name}", file=sys.stderr)
        except Exception as e:
            print(f"获取输入名称失败，使用默认名称: {e}", file=sys.stderr)
            input_name = "eager_tmp_0"
        
        # 获取实际的输出名称
        try:
            output_name = session.get_outputs()[0].name
            print(f"使用实际输出名称: {output_name}", file=sys.stderr)
        except Exception as e:
            print(f"获取输出名称失败，使用默认名称: {e}", file=sys.stderr)
            output_name = "fetch_name_0"
        
        # 打印输入数组的形状和类型
        print(f"输入数组形状: {image_array.shape}, 类型: {image_array.dtype}", file=sys.stderr)
        
        # 执行推理
        try:
            outputs = session.run([output_name], {input_name: image_array.astype(np.float32)})
            print(f"推理执行成功，输出形状: {outputs[0].shape}", file=sys.stderr)
        except Exception as e:
            print(f"推理执行失败: {e}", file=sys.stderr)
            return "推理执行失败", 0.0
        
        # 获取预测结果
        predictions = outputs[0][0]
        print(f"预测结果形状: {predictions.shape}, 值: {predictions}", file=sys.stderr)
        
        # 获取最大置信度的索引
        predicted_class = np.argmax(predictions)
        confidence = float(predictions[predicted_class])
        
        print(f"预测类别索引: {predicted_class}, 类别: {class_names[predicted_class]}, 置信度: {confidence}", file=sys.stderr)
        
        # 返回类别名称和置信度
        return class_names[predicted_class], confidence
    except Exception as e:
        error_msg = f"预测过程出错: {e}"
        print(error_msg, file=sys.stderr)
        return "预测失败", 0.0

def preprocess_image(image_file, target_size=(224, 224)):
    """
    预处理上传的图像
    
    参数:
        image_file: Django上传的图像文件
        target_size: 目标图像大小
    
    返回:
        numpy数组格式的预处理图像 - 格式为(batch_size, channels, height, width)
    """
    try:
        # 打开图像文件
        image = Image.open(image_file)
        
        # 转换为RGB模式（如果不是）
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 调整图像大小
        image = image.resize(target_size)
        
        # 转换为numpy数组
        image_array = np.array(image)
        
        # 归一化像素值
        image_array = image_array / 255.0
        
        # 扩展维度以添加批次维度
        image_array = np.expand_dims(image_array, axis=0)
        
        # 转换为通道优先格式 (batch_size, channels, height, width)
        # 因为ONNX模型期望输入为float32[1,3,224,224]
        image_array = np.transpose(image_array, (0, 3, 1, 2))
        
        return image_array
    except Exception as e:
        print(f"图像预处理失败: {e}")
        # 返回一个默认的零数组，以避免在处理失败时崩溃
        return np.zeros((1, 3, 224, 224), dtype=np.float32)