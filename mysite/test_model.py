import onnxruntime
import numpy as np
import os

# 模型路径
model_path = os.path.join(os.path.dirname(__file__), 'resnet50_garbage_final.onnx')
print(f"测试模型路径: {model_path}")

# 检查文件是否存在
if not os.path.exists(model_path):
    print("错误: 模型文件不存在!")
else:
    print(f"模型文件存在，大小: {os.path.getsize(model_path)} 字节")
    
    try:
        print(f"onnxruntime版本: {onnxruntime.__version__}")
        print("尝试加载模型...")
        session = onnxruntime.InferenceSession(model_path)
        print("模型加载成功!")
        
        # 获取输入信息
        input_info = session.get_inputs()[0]
        print(f"输入名称: {input_info.name}")
        print(f"输入形状: {input_info.shape}")
        print(f"输入类型: {input_info.type}")
        
        # 获取输出信息
        output_info = session.get_outputs()[0]
        print(f"输出名称: {output_info.name}")
        print(f"输出形状: {output_info.shape}")
        print(f"输出类型: {output_info.type}")
        
        # 创建一个测试输入
        test_input = np.zeros(input_info.shape, dtype=np.float32)
        print(f"创建测试输入，形状: {test_input.shape}")
        
        # 运行推理测试
        print("执行推理测试...")
        outputs = session.run([output_info.name], {input_info.name: test_input})
        print(f"推理成功! 输出形状: {outputs[0].shape}")
        print(f"输出样例: {outputs[0][0]}")
        
    except Exception as e:
        print(f"加载模型时出错: {e}")
        import traceback
        traceback.print_exc()