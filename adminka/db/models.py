from django.db import models


# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255, verbose_name="Категория")

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['category_name', 'category_id']



class Tovar(models.Model):
    tovar_id = models.AutoField(primary_key=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    tovar_name = models.CharField(max_length=255, verbose_name='Название товара')
    tovar_price = models.IntegerField(verbose_name="Цена")
    tovar_disc = models.TextField(blank=True, verbose_name="Описание")
    tovar_photo = models.ImageField(upload_to="photos/", verbose_name="фото", max_length=100, blank=True)

    def __str__(self):
        return self.tovar_name

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
        ordering = ['tovar_name', 'tovar_price', 'tovar_id']


# python manage.py makemigrations