from django.forms.models import model_to_dict
# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.models import Product

from products.serializers import ProductSerializers

# Create your views here.

# @api_view(['GET'])
# def api_home(request, *args, **kwargs):
#     instance = Product.objects.all().order_by('?').first()
#     data =  {}
#     if instance:
#         # model_to_dict converts the data base model in to a dictionary
#         # data = model_to_dict(instance, fields=['id', 'title', 'price', 'sale_price']) #using the model to dict to serialize the data from the model
#         # fields allows you to specify which fields you want to convert 
#         # to a dictionary and which you don't
#         data = ProductSerializers(instance).data
#     return Response(data)

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    # data = request.data
    serializer = ProductSerializers(data=request.data) # using a serializer tho validate the incoming data from the post request
    if serializer.is_valid(raise_exception=True): #raise_exception will catch if the data violates any of the model rules
        # instance = serializer.save() # when you save the data like this it commits it to the data base and returns a model of the saved serializer class
        print(serializer.data)
        # print(data.get_discount())
        # data = serializer.data
        return Response(serializer.data)
    return Response({'invalid': 'Not good data'}, status=400)