from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    badge = models.CharField(max_length=80, blank=True)
    subtitle = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    price = models.CharField(max_length=60)
    status = models.CharField(max_length=60, default='Available')
    server = models.CharField(max_length=80, blank=True)
    account_level = models.CharField(max_length=80, blank=True)
    summary = models.TextField(blank=True)
    delivery_note = models.CharField(
        max_length=160,
        blank=True,
        default='Direct WhatsApp handover after payment confirmation.',
    )
    cover_image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    store_name = models.CharField(max_length=80, default='Gameslot')
    title = models.CharField(max_length=120, default='New Season Stock')
    headline = models.CharField(max_length=180, default='No Reroll, No Life')
    description = models.TextField(
        default='Starter accounts, VIP collections, and reroll picks refreshed for anime game players.'
    )
    cover_image = models.ImageField(upload_to='site/', blank=True, null=True)
    announcement = models.CharField(
        max_length=160,
        blank=True,
        default='Fresh accounts are reviewed and updated regularly.',
    )
    whatsapp_number = models.CharField(max_length=24, default='60102431634')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Frontend Home Cover'
