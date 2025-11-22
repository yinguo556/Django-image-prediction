from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ImageUploadForm
from .models import UploadedImage
from .utils import preprocess_image, model_predict
from django.utils import timezone
import os

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            with open(uploaded_image.image.path, 'rb') as f:
                preprocessed_image = preprocess_image(f)
                prediction_class, confidence = model_predict(preprocessed_image)
                uploaded_image.prediction_result = f"类别: {prediction_class}, 置信度: {confidence:.2f}"
                uploaded_image.predicted_at = timezone.now()
                uploaded_image.save()
            return redirect('results', image_id=uploaded_image.id)
    else:
        form = ImageUploadForm()
    return render(request, 'garbage_app/upload.html', {'form': form})

def view_results(request, image_id):
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
        return render(request, 'garbage_app/results.html', {'image': uploaded_image})
    except UploadedImage.DoesNotExist:
        return render(request, 'garbage_app/error.html', {'message': '找不到指定的图像'})

def get_prediction_api(request, image_id):
    try:
        uploaded_image = UploadedImage.objects.get(id=image_id)
        return JsonResponse({
            'image_id': uploaded_image.id,
            'prediction': uploaded_image.prediction_result,
            'predicted_at': uploaded_image.predicted_at.isoformat() if uploaded_image.predicted_at else None
        })
    except UploadedImage.DoesNotExist:
        return JsonResponse({'error': 'Image not found'}, status=404)