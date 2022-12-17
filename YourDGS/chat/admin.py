from django.contrib import admin
from .models import Stock
# Register your models here.

class StockAdmin(admin.ModelAdmin):
    list_display = ('name','message','created_at')
    list_display_links = ('name','message','created_at')
admin.site.register(Stock,StockAdmin)