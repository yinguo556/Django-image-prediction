from django.db import models
from django.utils import timezone
import os

# 为上传的图片生成唯一文件名
def user_upload_to(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 生成新的文件名，包含时间戳以确保唯一性
    filename = f'{timezone.now().timestamp()}.{ext}'
    # 返回完整路径
    return os.path.join('uploads', filename)

class UploadedImage(models.Model):
    """上传图片的模型"""
    # 上传的图片文件
    image = models.ImageField(upload_to=user_upload_to)
    # 上传时间
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # 预测结果（可以是JSONField以存储更复杂的结果，但这里使用CharField简化）
    prediction_result = models.CharField(max_length=500, blank=True, null=True)
    # 预测时间
    predicted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"