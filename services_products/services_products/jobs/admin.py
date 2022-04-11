from django.contrib import admin

from services_products.jobs.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_types', 'date_of_publish')