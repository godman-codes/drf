import random
from django.db import models
from django.conf import settings
from django.db.models import Q
from rest_framework.reverse import reverse

User = settings.AUTH_USER_MODEL # just a string to auth.user

TAGS_MODEL_VALUES = ['electronics', 'cars', 'boats', 'movies', 'camera']
class ProductQuerySet(models.QuerySet):

    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query) # this will check both title and content
        qs = self.is_public().filter(lookup) # this checks the database for the lookup and also checks if its public
        if user is not None:
            # qs = qs.filter(user=user) # if there is a user you filter further down with the user
            qs2 = self.filter(user=user).filter(lookup) # this checks for the lookup in the data the user owns
            qs = (qs | qs2).distinct() # this merges the two so it can return not only public data but also private data that the user owns
        return qs

class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProductQuerySet(self.model, using=self._db) # this is where you can make use od another database loo further in to this too  

    def search(self, query, user=None):
        return self.get_queryset().search(query=query, user=user) # get_query set is a method built om to the model manager to get the query set

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL) # dont use related name because it will bring error when you use product_set.all()
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=99.99)
    public = models.BooleanField(default=True)
    objects =  ProductManager() # this will allow all methods defined in the product manager callable from the view on the model class

    def is_public(self):
        '''
        this meant to return a boolean value
        '''
        return self.public

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)] # getting a random choice from the TAGS_MODEL_VALUES list

    @property
    def body(self):
        '''
        in case you want to change the name of content without doing that to the model
        you will also be able to create and update but on the json input it will be body not content
        '''
        return self.content

    def get_absolute_url(self):
        return f'/api/product/{self.pk}'

    @property
    def url(self):
        return self.get_absolute_url()

    
    @property
    def path(self):
        return f"/product/{self.pk}/"

    @property
    def sale_price(self):
        '''
        the point of having this function is for added flexibility
        '''
        return round(float(self.price) * 0.9, 2)

    def get_discount(self):
        '''
        instance method
        '''
        return '122'
    
    def __repr__(self) -> str:
        return f"product: {self.title}"
