from django.urls import path

from services_products.products.views import ProductCreateView, ProductListView, ProductDetailsView, EditProductView, \
    DeleteProductView, ViewOwnProductList

urlpatterns = [
    path('create', ProductCreateView.as_view(), name="create product"),
    path('list', ProductListView.as_view(), name="list products"),
    path('view/<int:pk>', ProductDetailsView.as_view(), name="product details"),
    path('view/own/', ViewOwnProductList.as_view(), name='view own products'),
    path('edit/<int:pk>', EditProductView.as_view(), name="edit product"),
    path('delete/<int:pk>', DeleteProductView.as_view(), name="delete product")

]