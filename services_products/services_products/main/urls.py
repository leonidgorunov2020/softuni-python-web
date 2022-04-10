
from django.contrib import admin
from django.urls import path

from services_products.main.views import HomeView, ProductReview, ServiceReview, JobReview, BecomeDev, About

urlpatterns = [
    path('', HomeView.as_view(), name='show index'),
    path('product-review/', ProductReview.as_view(), name='product review'),
    path('service-review/', ServiceReview.as_view(), name='service review'),
    path('job-review/', JobReview.as_view(), name="job review"),
    path('become-dev/', BecomeDev.as_view(), name="become dev"),
    path('about/', About.as_view(), name="about us")
]
