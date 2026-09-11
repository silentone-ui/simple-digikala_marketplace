from django.db import models
from django.conf import settings


# ============================================================
# مدل دسته‌بندی (Category)
# ============================================================
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته بندی')
    slug = models.SlugField(unique=True, max_length=100, verbose_name='نامک')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات محصول')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


# ============================================================
# مدل محصول (Product)
# ============================================================
class Product(models.Model):
    # -------- کلید خارجی به دسته‌بندی --------
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='دسته بندی',
    )

    # -------- کلید خارجی به فروشگاه --------
    # 👇 این فیلد جدید اضافه شد (به جای seller)
    # چون هر محصول باید بدونه مال کدوم فروشگاهه
    store = models.ForeignKey(
        'stores.Store',              # ← مسیر ماژول به صورت رشته
        on_delete=models.CASCADE,
        related_name='products',     # ← از طرف store: store.products.all()
        verbose_name='فروشگاه',
    )

    name = models.CharField(max_length=255, verbose_name='نام محصول')
    slug = models.SlugField(unique=True, max_length=255, verbose_name='نامک')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='قیمت')
    stock = models.PositiveIntegerField(default=0, verbose_name='موجودی انبار')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='تصویر محصول')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین ویرایش')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='کاربر',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید'

    def __str__(self):
        return f"سبد {self.user}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',        
        verbose_name='سبد',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='محصول',
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')

    class Meta:
        verbose_name = 'آیتم سبد'
        verbose_name_plural = 'آیتم‌های سبد'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity