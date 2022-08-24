from rest_framework import serializers
from .models import Product
from rest_framework.validators import UniqueValidator

def validate_title(value): # to validate a field value we create a function with validate as prefix followed by an underscore e.g validate_<fieldname>(self, value)
        qs = Product.objects.filter(title__iexact=value) # title__exact is case sensitive while title__iexact is case insensitive
        if qs.exists():
            raise serializers.ValidationError(f"{value} is already a product name")
        return value

def validate_title_no_hello(value):
    if 'hello' == value.lower():
        raise serializers.ValidationError(f"{value} is not allowed")
    return value

unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact') # this will make ths validator to be case insensitive