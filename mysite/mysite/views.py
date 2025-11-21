from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageUploadForm
from .models import UploadedImage
from .utils import preprocess_image, model_predict
from django.utils import timezone
import os

def upload_image(request):
    """
    处理图片上传和预测的视图函数
    """
    if request.method == 'POST':
        # 创建表单实例并绑定数据
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # 保存上传的图像
            uploaded_image = form.save()
            
            # 打开并预处理图像
            with open(uploaded_image.image.path, 'rb') as f:
                # 预处理图像
                preprocessed_image = preprocess_image(f)
                
                # 调用模型进行预测
                prediction_class, confidence = model_predict(preprocessed_image)
                
                # 更新预测结果
                uploaded_image.prediction_result = f"类别: {prediction_class}, 置信度: {confidence:.2f}"
                uploaded_image.predicted_at = timezone.now()
                uploaded_image.save()
            
            # 重定向到结果页面
            return redirect('results', image_id=uploaded_image.id)
    else:
        # 创建空表单
        form = ImageUploadForm()
    
    # 渲染上传页面
    return render(request, 'upload.html', {'form': form})

def view_results(request, image_id):
    """
    显示预测结果的视图函数
    """
    try:
        # 获取上传的图像对象
        uploaded_image = UploadedImage.objects.get(id=image_id)
        
        # 渲染结果页面
        return render(request, 'results.html', {'image': uploaded_image})
    except UploadedImage.DoesNotExist:
        # 如果找不到图像，返回错误页面
        return render(request, 'error.html', {'message': '找不到指定的图像'})

def get_prediction_api(request, image_id):
    """
    提供预测结果的API端点（可选）
    """
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
        return JsonResponse({
            'image_id': uploaded_image.id,
            'prediction': uploaded_image.prediction_result,
            'predicted_at': uploaded_image.predicted_at.isoformat() if uploaded_image.predicted_at else None
        })
    except UploadedImage.DoesNotExist:
        return JsonResponse({'error': 'Image not found'}, status=404)