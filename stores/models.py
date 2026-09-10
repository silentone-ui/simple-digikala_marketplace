from django.db import models
from django.conf import settings

class Store(models.Model):
    name = models.CharField(max_length=255,verbose_name='نام فروشگاه')

    description = models.TextField(blank=True,null=True,verbose_name='توضیحات')

    website = models.URLField(max_length=200,blank=True,null=True,verbose_name='آدرسی وبسایت')

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='store',
        verbose_name='صاحب فروشگاه'
    )

    created_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='آخرین بریوز رسانی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه ها'