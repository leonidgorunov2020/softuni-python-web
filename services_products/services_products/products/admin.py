from django.contrib import admin

from services_products.jobs.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'date_of_release', 'price')
    