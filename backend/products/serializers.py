from rest_framework import serializers
# import serializers from rest framework 
from .models import Product

class ProductSerializers(serializers.ModelSerializers):
    '''
    create it like forms in normal django project the only difference
    is the serializers from the django framework
    '''
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
        ]

        def __repr__(self) -> str:
            return f'Product serializer'