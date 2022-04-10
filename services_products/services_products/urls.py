from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('services_products.main.urls')),
                  path('accounts/', include('services_products.accounts.urls')),
                  path('products/', include('services_products.products.urls')),
                  path('services/', include('services_products.services.urls')),
                  path('jobs/', include('services_products.jobs.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)