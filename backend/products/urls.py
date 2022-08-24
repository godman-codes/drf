from django.urls import path
# from .views import product_detail_view, product_create_view, product_Update_view
from .views import product_detail_view, product_list_create_view, product_Update_view, product_delete_view, product_mixin_view

urlpatterns = [
    path('<int:pk>/', product_detail_view, name='product-detail'),
    path('', product_list_create_view, name='product-list'),
    path('<int:pk>/update/', product_Update_view, name='product-update'),
    path('<int:pk>/delete/', product_delete_view, name='product_delete'),
    
]