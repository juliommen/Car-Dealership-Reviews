from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['car_make']
    inlines = [CarModelInline]


admin.site.register(CarMake, CarMakeAdmin)