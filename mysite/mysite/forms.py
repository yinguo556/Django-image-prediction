from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
        labels = {
            'image': '选择图片文件',
        }
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*',
            }),
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("图片大小不能超过5MB")
            
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
            extension = image.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError("请上传有效的图片文件（jpg, jpeg, png, gif, bmp）")
        
        return image