from django.forms.models import model_to_dict
# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product

from products.serializers import ProductSerializers

# Create your views here.

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    instance = Product.objects.all().order_by('?').first()
    data =  {}
    if instance:
        # model_to_dict converts the data base model in to a dictionary
        # data = model_to_dict(instance, fields=['id', 'title', 'price', 'sale_price']) #using the model to dict to serialize the data from the model
        # fields allows you to specify which fields you want to convert 
        # to a dictionary and which you don't
        data = ProductSerializers(instance).data
    return Response(data)