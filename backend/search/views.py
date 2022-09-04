from rest_framework import generics
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializers
from . import client
class SearchListView(generics.GenericAPIView):
    '''
    NOTE: if you print out request is a class <class 'rest_framework.request.Request'>
    while request.GET is also a class <class 'django.http.request.QueryDict'>
    '''
    def get(self, request, *args, **kwargs):
        user = None
        query = request.GET.get('q')
        tag = request.GET.get('tag') or None # this gets the parameters from the request objects which is tags 
        # print(type(request))
        if request.user.is_authenticated:
            user = request.user.username # this gets the parameters from the request objects which is users
        # print(str(request.GET.get('public')))
        public = str(request.GET.get('public') != '0') # this gets the parameters from the request objects which is public 
        # public = str(request.GET.get('public') or None) # this gets the parameters from the request objects which is public 
        # print(user, public, query, tag)
        if not query:
            return Response('', status=404)
        # if not tag: # so i later found out that without this condition my query wasn't working when there is no tag
        #     results = client.perform_search(query)
        #     return Response(results)
        results = client.perform_search(query, tags=[tag], user=user, public=public) # then we call the perform search operation passing query as query and tags as a **kwargs NOTE: tags is a list 
        return Response(results)

class SearchListOldView(generics.ListCreateAPIView):
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