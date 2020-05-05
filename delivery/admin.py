# delivery/admin.py

from django.contrib import admin

from delivery.models import (
    Category,
    Food
    )
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'is_sale')
    list_editable = ('price', 'is_sale')

admin.site.register(Category)

