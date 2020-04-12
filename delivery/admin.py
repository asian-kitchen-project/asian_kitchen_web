# delivery/admin.py

from django.contrib import admin

from delivery.models import (
    Category,
    Food
    )

admin.site.register(Category)
admin.site.register(Food)
