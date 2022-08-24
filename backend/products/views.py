from ast import Del
from rest_framework import authentication, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializers
from api.authentication import TokenAuthentication
from api.permissions import IsDeleteRolesPermission, IsStaffEditorPermission
from api.mixins import StaffEditorPermissionMixin, DeleteRolesPermissionMixin

class ProductDetailAPIView(generics.RetrieveAPIView):
    '''
    note: detail view gets just one single item
    '''
    permission_classes = [permissions.IsAdminUser ,IsStaffEditorPermission ,IsDeleteRolesPermission]
    authentication_classes= [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]
    queryset = Product.objects.all() #getting the query sets from the database
    serializer_class = ProductSerializers
    # lookup_field = 'pk'

product_detail_view = ProductDetailAPIView.as_view()

class ProductCreateAPIView(generics.CreateAPIView):
    '''
    create products
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


class ProductListCreateAPIView(
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView): 
    '''
    if request.method == 'POST': -> create new product
    if request.method == 'GET': -> list all products
    '''
    queryset = Product.objects.all() #getting the query sets from the database
    serializer_class = ProductSerializers # we can save the content to the database
    # authentication_classes = [] # this is to disable authentication by overriding the get_authentication_classes method
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     authentication.TokenAuthentication
    #     ] # this is the authentication class that will be used to authenticate the user
    # permission_classes = [permissions.IsAuthenticated] # this will make sure that only authenticated users can access this view
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly] # this will make sure that only authenticated users can change the data in the database
    # permission_classes = [permissions.IsAdminUser ,IsStaffEditorPermission ,IsDeleteRolesPermission]

    def perform_create(self, serializer):
        '''
        this function can only be called in the generic create class view
        and we can use it to manipulate the data we want to save to the data base
        '''
        # serializer.save(user=self.request.user) we can assign user like this 
        print(serializer.validated_data)
        # email = serializer.validated_data.pop('email') # this gets the email address and prevent it from being sent to the database
        # print(email)
        title = serializer.validated_data.get('title') # this gets the title from the from the validated serialized data
        content = serializer.validated_data.get('content') or None # this get the content and if the content isn't there it will return None  

        if not content:
            content = title # if the content is not there then we will assign the title to the content
        serializer.save(user=self.request.user, content=content) # we can save the content to the database and this will automatically grab the logged in user********************************
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        print(request.user)
        return qs.filter(user=request.user) # this will make the get list method only return values that are associated with the logged in user

product_list_create_view = ProductListCreateAPIView.as_view() # this is the view that will be used in the urls.py file


class ProductMixinView(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView
                    ):
    '''
        this is a mixin view
        Note in class base views we write functions for different methods
        while in function based views we write conditionals for different methods
    '''
    queryset = Product.objects.all() #getting the query sets from the database
    serializer_class = ProductSerializers # make sure this is serializer_class and not just serializer
    lookup_field = 'pk'
    
    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        pk = kwargs.get('pk') # this gets the pk from the url
        if pk is not None: # if the pk is not None then we will return the detail view
            return self.retrieve(request, *args, **kwargs) 
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs): # this is the create view
        
        return self.create(request, *args, **kwargs) # this is the create view

    def perform_create(self, serializer):
        '''
        this function can only be called in the generic create class view
        and we can use it to manipulate the data we want to save to the data base
        '''
        # serializer.save(user=self.request.user) we can assign user like this 
        print(serializer.validated_data)
        title = serializer.validated_data.get('title') # this gets the title from the from the validated serialized data
        content = serializer.validated_data.get('content') or None # this get the content and if the content isn't there it will return None

        if content is None:
            content = 'this is a view doing cool stuff' # if the content is not there then we will assign a string to the content
        serializer.save(content=content) # we can save the content to the database

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        

product_mixin_view = ProductMixinView.as_view()


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
    # permission_classes = [permissions.IsAdminUser ,IsStaffEditorPermission, IsDeleteRolesPermission]
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
    # permission_classes = [permissions.IsAdminUser ,IsStaffEditorPermission, IsDeleteRolesPermission] # checks if we have permissions to delete a product view
    '''
    permission_classes = [permissions.IsAdminUser, IsDeleteRolesPermission] # when there are two permissions in the permissions class arrays
    the first permission checker will be used before the preceding permission checker will be used    
    '''
    queryset = Product.objects.all() # getting the query sets from the database
    serializer_class = ProductSerializers # this is the serializer class that will be used to serialize the data
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # instance 
        super().perform_destroy(instance) # this will delete the instance from the database

product_delete_view = ProductDestroyAPIView.as_view()