from django.forms.models import model_to_dict
# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product

# Create your views here.

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by('?').first()
    data =  {}
    if model_data:
        # model_to_dict converts the data base model in to a dictionary
        data = model_to_dict(model_data, fields=['id', 'title', 'price', 'sale_price'])
        # fields allows you to specify which fields you want to convert to a dictionary and which you don't
    return Response(data)