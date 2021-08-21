from django.contrib import admin
from .models import Room


class GeneralAdmin(admin.ModelAdmin):
    list_display = ['title', 'address', 'landlord', 'size', 'is_available',
                    'is_approved', 'rent', 'bond_amount', 'status', 'list_date']
    list_display_links = ['title', 'landlord']
    list_editable = ['is_available', 'is_approved', ]

    # def has_add_permission(self, request):
    #   return False


admin.site.register(Room, GeneralAdmin)
