from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    """图片上传表单"""
    class Meta:
        model = UploadedImage
        fields = ['image']
        # 自定义表单字段的标签和小部件属性
        labels = {
            'image': '选择图片文件',
        }
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',  # 限制只能上传图片文件
            }),
        }
    
    def clean_image(self):
        """验证上传的文件是否为有效的图片"""
        image = self.cleaned_data.get('image')
        
        if image:
            # 检查文件大小（这里限制为5MB）
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("图片大小不能超过5MB")
            
            # 检查文件扩展名
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
            extension = image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("请上传有效的图片文件（jpg, jpeg, png, gif, bmp）")
        
        return image