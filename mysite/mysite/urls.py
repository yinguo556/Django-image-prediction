from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.upload_image, name='upload'),
    path('results/<int:image_id>/', views.view_results, name='results'),
    path('api/prediction/<int:image_id>/', views.get_prediction_api, name='prediction_api'),
]

# 添加媒体文件URL路由，移除DEBUG条件，使生产环境也能访问
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
