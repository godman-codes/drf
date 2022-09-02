from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer
from .models import Product
from .validators import validate_title, validate_title_no_hello, unique_product_title
from api.serializers import UserProductInlineSerializer
class ProductSerializers(serializers.ModelSerializer):
    '''
    create it like forms in normal django project the only difference
    is the serializers from the django framework
    '''
    owner = UserPublicSerializer(source='user', read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'pk'
    ) # this can also be used for creating url links for each product for redirection to different views
    # my_discount = serializers.SerializerMethodField(read_only=True) #this is meant to look for 
    # get_<attribute name> which is meant to be get_discount but it can't find it 
    # so we count instance a self class for this class and name it get_discount
    # to initiate that get_discount attribute
    # so we changed it from get discount to my_discount which will now look for 
    # the attribute get_my_discount
    # email = serializers.EmailField(write_only=True) # without additional configuration this serializer class 
    # will try to create this attribute in the model but will meet an error because the email attribute is not in our product model
    # email = serializers.EmailField(source='user.email', read_only=True) # the use of source here can be used to grab the email of the user associated with this product models
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(validators=[validate_title_no_hello, unique_product_title]) # the title attribute will validate against the imported validation function from validate.py 
    name = serializers.CharField(source='title', read_only=True) # this creates a read only field that is gets its value from the title and maybe it only works with attributes in the database model
    # other_products = UserProductInlineSerializer(source='user.product_set.all', read_only=True, many=True) # the source grabs it from the tables relationship to the user tables
    public = serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields = [
            # 'user', # since we are automatically grabbing the logged in user we don't need to display it as fields in our serializers
            'owner', 
            'edit_url',
            'url',
            # 'email',
            'pk',
            'title',
            'content',
            'name',
            'price',
            'sale_price',
            'public',
            # 'my_discount', #changed this from get_discount to discount and it raised an error because it could not get the get discount function from the product model class
            # 'my_user_data',
            # 'other_products'
        ]

        def __repr__(self) -> str:
            return f'Product **serializer'


    # def get_other_products(self, obj):
    #     print(obj.user)
    #     my_products_qs = self.user.product_set.all()
    #     return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data
    
    
    def get_my_user_data(self, obj):
        return {
            "username": obj.user.username,
        }
    # def validate_title(self, value): # to validate a field value we create a function with validate as prefix followed by an underscore e.g validate_<fieldname>(self, value)
    #     qs = Product.objects.filter(title__iexact=value) # title__exact is case sensitive while title__iexact is case insensitive
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    # def create(self, validated_data):
    #     # return Product.objects.create(**validated_data) # note the double asterisk used to unpack an object
    #     # print(validated_data)
    #     # email = validated_data.pop('email') # this prevents the email from being sent to the product model class
    #     obj = super().create(validated_data)
    #     # print(email, obj)
    #     return obj

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title')
    #     email = validated_data.pop('email') # this gets the email address
    #     return instance
            

    def get_edit_url(self, obj):
        '''
        the use of reverse will make this url relative to the product model class
        so url will be an active link
        Note: this function adds an active link to the product model class
        '''
        # return f"/api/product/{obj.pk}/"
        # print(self.context)
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-update", kwargs = {'pk': obj.pk}, request=request)
    
    def get_my_discount(self, obj):
        '''
        this method takes the two attribute the productSerializer class it's in
        and the database model object and instantiate the get_discount method associated with the method
        '''
        '''
        this returning AttributeError: 'collections.OrderedDict' object has no attribute 'get_discount'because we haven't saved the data to the model so we 
        cannot access obj.get_discount()
        we can handle this withe except or hasattr method or isinstance method
        '''
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()

'''
note: we can have multiple serializers for one model class by changing the class name eg. PrimaryModelSerializers, SecondaryModelSerializers e.t.c
and customize them any how we like 
'''