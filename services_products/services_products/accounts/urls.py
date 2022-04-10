from django.contrib.auth.views import LogoutView
from django.urls import path

from services_products.accounts.views import UserLoginView, UserDetailsView, UserRegisterView, EditUserView, \
    ChangeUserPasswordView, DeleteUserView, LastViewedProduct

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', LogoutView.as_view(), name='logout user'),
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('edit/<int:pk>', EditUserView.as_view(), name='edit user'),
    path('password/change/', ChangeUserPasswordView.as_view(), name='change user password'),
    path('profile/view/<int:pk>', UserDetailsView.as_view(), name='profile view'),
    path('last-viewed-product/', LastViewedProduct.as_view(), name='last viewed product'),
    path('delete/<int:pk>', DeleteUserView.as_view(), name='delete profile')
]
