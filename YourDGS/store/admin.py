from django.contrib import admin
from.models import Product,Variation,ReviewRating
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ['admin_photo','product_name','price','stock','category','subcategory','modified_date','created_date','is_available']
    list_display_links = ('product_name',)
    list_filter = ('product_name','category','subcategory')
    search_fields = ['product_name','category','subcategory']
    readonly_fields = ['admin_photo']
    list_per_page = 10


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active', )
    list_filter = ('product', )

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)