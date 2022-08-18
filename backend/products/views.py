from rest_framework import generics

from .models import Product
from .serializers import ProductSerializers

class ProductDetailAPIView(generics.RetrieveAPIView):
    '''
    note: detail view gets just one single item
    '''
    queryset = Product.objects.all() #getting the query sets from the database
    serializer_class = ProductSerializers
    # lookup_field = 'pk'

product_detail_view = ProductDetailAPIView.as_view()

class ProductCreateAPIView(generics.CreateAPIView):
    '''
    cerate view
    '''
    queryset = Product.objects.all() #getting the query sets from the database
    serializer_class = ProductSerializers

    def perform_create(self, serializer):
        '''
        this function can only be called in the generic create class view
        and we can use it to manipulate the data we want to save to the data base
        '''
        # serializer.save(user=self.request.user) we can assign user like this 
        print(serializer.validated_data)
        title = serializer.validated_data.get('title') # this gets the title from the from the validated serialized data
        content = serializer.validated_data.get('content') or None # this get the content and if the content isn't there it will return None  

        if not content:
            content = title # if the content is not there then we will assign the title to the content
        serializer.save(content=content) # we can save the content to the database

product_create_view = ProductCreateAPIView.as_view() # this is the view that will be used in the urls.py file


class ProductUpdateAPIView(generics.UpdateAPIView):
    '''
    cerate view
    '''
    queryset = Product.objects.all() # getting the query sets from the database
    serializer_class = ProductSerializers # this is the serializer class that will be used to serialize the data
    # lookup_field = 'pk'

product_Update_view = ProductUpdateAPIView.as_view()




