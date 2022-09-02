from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL # just a string to auth.user

class ProductQuerySet(models.QuerySet):

    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query) # this will check both title and content
        qs = self.filter(lookup) 
        if user is not None:
            qs = qs.filter(user=user) # if there is a user you filter further down with the user
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
    public = models.BooleanField(default=False)

    @property
    def sale_price(self):
        return round(float(self.price) * 0.9, 2)

    def get_discount(self):
        '''
        instance method
        '''
        return '122'
    
    def __repr__(self) -> str:
        return f"product: {self.title}"
