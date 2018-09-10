from rest_framework import mixins
from rest_framework import viewsets

from .functions import predict_image, update_real_label


# Create your views here.
class ModelViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        response = predict_image(request)
        return response

    def update(self, request, *args, **kwargs):
        response = update_real_label(self, request)
        return response
