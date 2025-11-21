import numpy as np
from PIL import Image
import io
import os
import sys

# 延迟导入onnxruntime，避免在模块加载时就尝试加载模型
rt = None

# 模型路径
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resnet50_garbage_final.onnx')
pass

class_names = [
    "纸张",
    "塑料",
    "玻璃"
]

def get_model_session():
    global rt
    
    # 动态导入onnxruntime
    if rt is None:
        try:
            import onnxruntime
            rt = onnxruntime  # 更新全局变量
            pass
        except ImportError as e:
            pass
            return None
    
    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        pass
        return None
    else:
        pass
    
    try:
        # 尝试创建推理会话，添加更多的错误捕获
        pass
        session = rt.InferenceSession(model_path)
        pass
        return session
    except Exception as e:
        pass
        return None

def model_predict(image_array):
    try:
        # 获取模型会话（懒加载）
        session = get_model_session()
        
        # 如果模型未加载成功，返回默认值
        if session is None:
            pass
            return "模型加载失败", 0.0
        
        # 获取实际的输入名称
        try:
            input_name = session.get_inputs()[0].name
        except Exception:
            input_name = "eager_tmp_0"
        
        # 获取实际的输出名称
        try:
            output_name = session.get_outputs()[0].name
        except Exception:
            output_name = "fetch_name_0"
        
        # 打印输入数组的形状和类型
        pass
        
        # 执行推理
        try:
            outputs = session.run([output_name], {input_name: image_array.astype(np.float32)})
        except Exception:
            return "推理执行失败", 0.0
        
        # 获取预测结果
        predictions = outputs[0][0]
        pass
        
        # 获取最大置信度的索引
        predicted_class = np.argmax(predictions)
        confidence = float(predictions[predicted_class])
        
        pass
        
        # 返回类别名称和置信度
        return class_names[predicted_class], confidence
    except Exception as e:
        pass
        return "预测失败", 0.0

def preprocess_image(image_file, target_size=(224, 224)):
    try:
        # 打开图像文件
        image = Image.open(image_file)
        
        # 转换为RGB模式（如果不是）
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 获取原始尺寸
        width, height = image.size
        pass
        
        # 检查是否为极小图像（<100×100），如果是则加白框
        if width < 100 or height < 100:
            pass
            # 创建224×224的白色背景图像
            new_image = Image.new('RGB', (224, 224), color='white')
            
            # 计算粘贴位置（居中）
            paste_x = (224 - width) // 2
            paste_y = (224 - height) // 2
            
            # 将原图粘贴到白色背景上
            new_image.paste(image, (paste_x, paste_y))
            image = new_image
        else:
            # 按比例缩放，使短边变为224
            min_dim = min(width, height)
            scale_factor = 224 / min_dim
            
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            pass
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 中心裁剪224×224
            left = (new_width - 224) // 2
            top = (new_height - 224) // 2
            right = left + 224
            bottom = top + 224
            
            pass
            image = image.crop((left, top, right, bottom))
        
        # 转换为numpy数组
        image_array = np.array(image)
        
        # 归一化像素值
        image_array = image_array / 255.0
        
        # 扩展维度以添加批次维度
        image_array = np.expand_dims(image_array, axis=0)
        
        # 转换为通道优先格式 (batch_size, channels, height, width)
        # 因为ONNX模型期望输入为float32[1,3,224,224]
        image_array = np.transpose(image_array, (0, 3, 1, 2))
        
        pass
        return image_array
    except Exception as e:
        pass
        # 返回一个默认的零数组，以避免在处理失败时崩溃
        return np.zeros((1, 3, 224, 224), dtype=np.float32)