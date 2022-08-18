from django.urls import path
# from .views import product_detail_view, product_create_view, product_Update_view
from .views import product_detail_view, product_list_create_view, product_Update_view, product_alt_view

urlpatterns = [
    path('<int:pk>/', product_alt_view),
    path('', product_alt_view),
    # path('<int:pk>/update/', product_Update_view)
]