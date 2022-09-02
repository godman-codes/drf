from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product

@register(Product) # this is very similar to the normal django admin.site.register(Product, ProductModelAdmin)
class ProductIndex(AlgoliaIndex):
    """
    this field will be mapped to its equivalent in the serializer class
    NOTE: you dont want to add relevant and secured in formations to algolia
    """
    should_index = 'is_public'
    fields = [
        'title',
        'content',
        'price',
        'user',
        'public'
    ]