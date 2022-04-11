from django.contrib import admin

from services_products.products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'date_of_release', 'price')
