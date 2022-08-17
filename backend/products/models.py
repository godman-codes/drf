from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=99.99)

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
