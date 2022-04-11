from django.contrib import admin

from services_products.services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cycle', 'date_of_publish', 'fee')

    