from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializers

class SearchListView(generics.ListCreateAPIView):
    queryset = Product.object.all()
    serializer_class = ProductSerializers
    