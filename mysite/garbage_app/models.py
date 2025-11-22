from django.db import models
from django.utils import timezone
import os

def user_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{timezone.now().timestamp()}.{ext}'
    return os.path.join('uploads', filename)

class UploadedImage(models.Model):
    image = models.ImageField(upload_to=user_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    prediction_result = models.CharField(max_length=500, blank=True, null=True)
    predicted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"