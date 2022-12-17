from django.contrib import admin
from category.models import Category,SubCategory

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ['admin_photo','category_name']
    list_display_links = ('category_name',)
    list_filter = ('category_name',)
    search_fields = ['category_name']
    readonly_fields = ['admin_photo']
    list_per_page = 10

admin.site.register(Category, CategoryAdmin)



class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name','category','created_at','updated_at']
    list_display_links = ('name',)
    list_filter = ('name','category')
    search_fields = ['name','category']
    list_per_page = 50

admin.site.register(SubCategory, SubCategoryAdmin)
