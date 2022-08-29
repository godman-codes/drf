from rest_framework import serializers

class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'pk',
        read_only = True,
    ) # this can also be used for creating url links for each product for redirection to different views
    name = serializers.CharField(source='title', read_only=True) # this creates a read only field that is gets its value from the title and maybe it only works with attributes in the database model

class UserPublicSerializer(serializers.Serializer):
    '''
    in the other serializer we put source='user' which the grabs the user.username and user.id fields
    '''
    username = serializers.CharField(read_only=True) 
    id = serializers.IntegerField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)

    # def get_other_products(self, obj):
    #     # print(obj)
    #     user = obj
    #     my_products_qs = user.product_set.all()
    #     return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data