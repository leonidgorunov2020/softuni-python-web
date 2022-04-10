from django.urls import path

from services_products.services.views import ServiceCreateView, ServiceListView, ServiceDetailsView, EditServiceView, \
    DeleteServiceView, ViewOwnServiceList

urlpatterns = [
    path('create/', ServiceCreateView.as_view(), name="create service"),
    path('list/', ServiceListView.as_view(), name="list services"),
    path('view/<int:pk>', ServiceDetailsView.as_view(), name="service details"),
    path('view/own', ViewOwnServiceList.as_view(), name='view own services'),
    path('edit/<int:pk>', EditServiceView.as_view(), name="edit service"),
    path('delete/<int:pk>', DeleteServiceView.as_view(), name="delete service")

]