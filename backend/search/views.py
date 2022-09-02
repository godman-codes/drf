from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializers

class SearchListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q') # this gets the query parameter aka the search parameter from the request object
        results = Product.objects.none() # this return if the query parameter is not specified
        if q is not None:
            user = None # by default without authentication the user is none
            if self.request.user.is_authenticated:
                user  = self.request.user # assign the user to the user variable
            results = qs.search(q, user=user) # this is the method defined in the Product manager class
        return results

search_list_view = SearchListView.as_view()