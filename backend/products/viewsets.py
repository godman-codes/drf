from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializers

class ProductViewSet(viewsets.ModelViewSet):
    '''
    get  -> list -> queryset
    get  -> retrieve -> Product instance detail view
    post -> create -> new instances
    put -> update -> 
    patch -> partial update -> partial update
    destroy -> delete instance 
    '''
    queryset = Product.objects.all() #getting the query sets from the database
    serializer_class = ProductSerializers # getting the serializer class
    lookup_field = 'pk'