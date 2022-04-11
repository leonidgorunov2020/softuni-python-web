from django.contrib import admin

from services_products.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('upper_case_name',)

    @admin.display(description='Name')
    def upper_case_name(self, obj):
        return ("%s %s" % (obj.first_name[0], obj.last_name[0])).upper()
