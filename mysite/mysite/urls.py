from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('garbage_app.urls')),  # 包含garbage_app的URL配置
]

# 添加媒体文件URL路由，移除DEBUG条件，使生产环境也能访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
