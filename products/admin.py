# products/admin.py

from django.contrib import admin
from .models import Country, Category, Subcategory, Product, Like, Comment, ProductView, Favorite

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'subcategory', 'country_of_origin', 'stock', 'views', 'condition')
    list_filter = ('category', 'subcategory', 'country_of_origin', 'condition', 'price')
    search_fields = ('name', 'description', 'category__name', 'subcategory__name', 'country_of_origin__name')
    readonly_fields = ('views',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name', 'text')

@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'product__name')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'product__name')
