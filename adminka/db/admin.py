from django.contrib import admin
from .models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)           # Доп поля
    list_display_links = ('category_name',)     # ССылка на Доп поля
    search_fields = ('category_name',)          # Поиск по


class TovarAdmin(admin.ModelAdmin):
    list_display = ('tovar_name', 'category', 'tovar_price', 'tovar_disc', 'tovar_photo')
    list_display_links = ('tovar_name', 'category', 'tovar_price', 'tovar_disc', 'tovar_photo')
    search_fields = ('tovar_name', 'category__category_name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tovar, TovarAdmin)



