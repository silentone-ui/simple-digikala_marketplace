from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='نام دسته بندی')
    slug = models.SlugField(unique=True,max_length=100,verbose_name='نامک')
    description = models.TextField(blank=True,null=True,verbose_name='توضیحات محصول')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='دسته بندی',
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='فروشنده',
    )
    name = models.CharField(max_length=255,verbose_name='نام محصول')
    slug = models.SlugField(unique=True,max_length=255,verbose_name='نامک')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=12,decimal_places=2,verbose_name='قیمت')
    stock = models.PositiveIntegerField(default=0,verbose_name='موجودی انبار')
    image = models.ImageField(upload_to='products/',blank=True,null=True,verbose_name='تصویر محصول')

    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='تاریخ اخرین ویرایش')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name