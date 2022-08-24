from rest_framework import serializers
from rest_framework.reverse import reverse
# import serializers from rest framework 
from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    '''
    create it like forms in normal django project the only difference
    is the serializers from the django framework
    '''
    url = serializers.SerializerMethodField(read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True) #this is meant to look for 
    # get_<attribute name> which is meant to be get_discount but it can't find it 
    # so we count instance a self class for this class and name it get_discount
    # to initiate that get_discount attribute
    # so we changed it from get discount to my_discount which will now look for 
    # the attribute get_my_discount
    class Meta:
        model = Product
        fields = [
            'url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount', #changed this from get_discount to discount and it raised an error because it cound not get the get discoun function from the product model class
        ]

        def __repr__(self) -> str:
            return f'Product **serializer'
            

    def get_url(self, obj):
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
        return reverse("product-detail", kwargs = {'pk': obj.pk}, request=request)
    
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