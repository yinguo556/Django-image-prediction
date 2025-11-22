from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload'),
    path('results/<int:image_id>/', views.view_results, name='results'),
    path('api/prediction/<int:image_id>/', views.get_prediction_api, name='prediction_api'),
]