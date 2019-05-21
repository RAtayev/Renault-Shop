from django.contrib import admin

# Register your models here.

from .models import Auto, Order

# admin.site.register(Auto)
# admin.site.register(Order)

class OrdersInline(admin.TabularInline):
    model = Order

class AutoAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    inlines = [OrdersInline]

admin.site.register(Auto, AutoAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(Order, OrderAdmin)