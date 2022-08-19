from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
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

# class ProductCreateAPIView(generics.CreateAPIView):
#     '''
#     create products
#     '''
#     queryset = Product.objects.all() #getting the query sets from the database
#     serializer_class = ProductSerializers

#     def perform_create(self, serializer):
#         '''
#         this function can only be called in the generic create class view
#         and we can use it to manipulate the data we want to save to the data base
#         '''
#         # serializer.save(user=self.request.user) we can assign user like this 
#         print(serializer.validated_data)
#         title = serializer.validated_data.get('title') # this gets the title from the from the validated serialized data
#         content = serializer.validated_data.get('content') or None # this get the content and if the content isn't there it will return None  

#         if not content:
#             content = title # if the content is not there then we will assign the title to the content
#         serializer.save(content=content) # we can save the content to the database

# product_create_view = ProductCreateAPIView.as_view() # this is the view that will be used in the urls.py file


class ProductListCreateAPIView(generics.ListCreateAPIView):
    '''
    if request.method == 'POST': -> create new product
    if request.method == 'GET': -> list all products
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

product_list_create_view = ProductListCreateAPIView.as_view() # this is the view that will be used in the urls.py file




@api_view(['GET', 'POST']) # this decorator allows us to use the same view for both get and post requests
def product_alt_view(request, pk=None, *args, **kwargs): # pk has to have a default value of none because we don't know the pk of the product yet
    '''
    this view is able to handle different http methods
    '''
    method = request.method # this will get the http method also  put -> update, delete -> destroy

    if method == 'GET':
        if pk is not None:
            # then this is a detail view
            obj = get_object_or_404(Product, pk=pk) # this will get the object or 404 if the object is not found
            data = ProductSerializers(obj, many=False).data # this will serialize the data and the many=False will make sure that it will return just one item note: always remember to put .data at the end of the serializer class
            return Response(data) # this will return the serialized data
            
        queryset = Product.objects.all() # getting the query sets from the database
        data = ProductSerializers(queryset, many=True).data # this is the serializer class that will be used to serialize the data and the many=True will make sure that it will return a list of items
        return Response(data)
        
    if method == 'POST':
        serializer = ProductSerializers(data=request.data) # using a serializer tho validate the incoming data from the post request
        if serializer.is_valid(raise_exception=True): # raise_exception will catch if the data violates any of the model rules
            # instance = serializer.save() # when you save the data like this it commits it to the data base and returns a model of the saved serializer class
            title = serializer.validated_data.get('title') # this gets the title from the from the validated serialized data
            content = serializer.validated_data.get('content') or None # this get the content and if the content isn't there it will return None  
            if not content:
                content = title # if the content is not there then we will assign the title to the content
            serializer.save(content=content) # we can save the content to the database
            # print(data.get_discount())
            # data = serializer.data
            return Response(serializer.data)
        return Response({'invalid': 'Not good data'}, status=400)


class ProductUpdateAPIView(generics.UpdateAPIView):
    '''
    update product view
    '''
    queryset = Product.objects.all() # getting the query sets from the database
    serializer_class = ProductSerializers # this is the serializer class that will be used to serialize the data
    lookup_field = 'pk'

    def perform_update(self, serializer):
        '''
        this function can only be called in the generic update class view
        and we can use it to manipulate the data we want to save to the data base
        '''
        instance = serializer.save() # this will save the data to the database
        if not instance.content:
            instance.content = instance.title
            

product_Update_view = ProductUpdateAPIView.as_view()

class ProductDestroyAPIView(generics.DestroyAPIView):
    '''
    Destroy product view
    '''
    queryset = Product.objects.all() # getting the query sets from the database
    serializer_class = ProductSerializers # this is the serializer class that will be used to serialize the data
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # instance 
        super().perform_destroy(instance) # this will delete the instance from the database

product_delete_view = ProductDestroyAPIView.as_view()