
# blog/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.urls import reverse

class Category(models.Model):
    kind = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.kind


class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(
        upload_to='food_images/', null=True, blank=True)
    is_sale = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_sale and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer = models.CharField(
        verbose_name='顧客名',
        max_length=100,
    )

    sub_total = models.IntegerField(
        verbose_name='小計',
    )

    tax = models.IntegerField(
        verbose_name='消費税',
    )

    total_amount = models.IntegerField(
        verbose_name='合計金額',
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='作成者',
    )

    created_at = models.DateTimeField(
        verbose_name='登録日',
        auto_now_add=True
    )

    def __str__(self):
        return self.customer

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE)

    food = models.ForeignKey(
        Food,
        verbose_name='商品',
        on_delete=models.CASCADE,
    )

    unit_price = models.IntegerField(
        verbose_name='単価',
        validators=[validators.MinValueValidator(0)],
    )

    quantity = models.IntegerField(
        verbose_name='数量',
        validators=[validators.MinValueValidator(0)],
    )

    amount = models.IntegerField(
        verbose_name='金額',
    )
