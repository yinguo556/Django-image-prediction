from django.contrib import admin
from .models import UploadedImage

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    """
    自定义UploadedImage模型的管理界面
    """
    # 列表页显示的字段
    list_display = ('id', 'image_thumbnail', 'uploaded_at', 'predicted_at', 'prediction_preview')
    
    # 可搜索字段
    search_fields = ('prediction_result',)
    
    # 过滤条件
    list_filter = ('uploaded_at', 'predicted_at')
    
    # 详情页显示的字段
    fields = ('image', 'uploaded_at', 'prediction_result', 'predicted_at')
    
    # 只读字段
    readonly_fields = ('uploaded_at', 'predicted_at')
    
    # 列表页每页显示数量
    list_per_page = 20
    
    def image_thumbnail(self, obj):
        """
        在列表页显示图片缩略图
        """
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "无图片"
    image_thumbnail.short_description = '图片预览'
    image_thumbnail.allow_tags = True
    
    def prediction_preview(self, obj):
        """
        在列表页显示预测结果的前50个字符
        """
        if obj.prediction_result:
            return obj.prediction_result[:50] + ("..." if len(obj.prediction_result) > 50 else "")
        return "无预测结果"
    prediction_preview.short_description = '预测结果'

# 注册其他模型（如果有）
# admin.site.register(OtherModel)