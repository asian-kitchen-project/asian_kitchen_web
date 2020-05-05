# delivery/admin.py

from django.contrib import admin

from delivery.models import (
    Category,
    Food,
    Invoice,
    InvoiceDetail
    )

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'is_sale')
    list_editable = ('price', 'is_sale')

class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 0

admin.site.register(Category)

# admin.site.register(InvoiceDetail)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceDetailInline]
