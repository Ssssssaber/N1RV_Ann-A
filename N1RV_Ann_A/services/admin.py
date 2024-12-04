from django.contrib import admin
from .models import Hairdresser, Service, OrderedServices

# Register your models here.
@admin.register(Hairdresser)
class HairdresserAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderedServices)
class OrderedServicesAdmin(admin.ModelAdmin):
    pass