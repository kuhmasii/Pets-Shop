from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created", "updated")
    list_filter = ('created', 'updated')
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ("category", "name", "price", "_discount",
                    "shipping", "in_stock", "created", "updated")
    list_filter = ("category", "price", "_discount",
                   "shipping", "in_stock", "created", "updated")
    list_editable = ("shipping", "price", "in_stock", "_discount")
    prepopulated_fields = {'slug': ('name', 'category',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
