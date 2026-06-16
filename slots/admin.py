from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, SiteSetting

admin.site.site_header = 'Gameslot Store Administration'
admin.site.site_title = 'Gameslot Admin'
admin.site.index_title = 'Store Management'


def image_source(image=None, external_url=''):
    if image:
        return image.url
    return external_url or ''


def image_preview(image=None, external_url='', size=54):
    src = image_source(image, external_url)
    if not src:
        return '-'
    return format_html(
        '<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:6px;" />',
        src,
        size,
        size,
    )


@admin.action(description='Publish selected items')
def publish_items(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description='Unpublish selected items')
def unpublish_items(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'name', 'slug', 'badge', 'product_count', 'accent_color', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'badge', 'subtitle')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('accent_color', 'is_active', 'sort_order')
    readonly_fields = ('large_cover_preview', 'created_at', 'updated_at')
    actions = (publish_items, unpublish_items)
    fieldsets = (
        ('Category', {'fields': ('name', 'slug', 'badge', 'subtitle', 'description', 'accent_color')}),
        ('Frontend Cover', {'fields': ('cover_image', 'image_url', 'large_cover_preview')}),
        ('Publishing', {'fields': ('is_active', 'sort_order')}),
        ('Dates', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Cover')
    def cover_preview(self, obj):
        return image_preview(obj.cover_image, obj.image_url)

    @admin.display(description='Cover preview')
    def large_cover_preview(self, obj):
        return image_preview(obj.cover_image, obj.image_url, 220)

    @admin.display(description='Listings')
    def product_count(self, obj):
        return obj.products.count()


@admin.action(description='Mark selected products as featured')
def mark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description='Remove selected products from featured')
def unmark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


@admin.action(description='Mark selected products as hot')
def mark_hot(modeladmin, request, queryset):
    queryset.update(is_hot=True)


@admin.action(description='Remove hot badge')
def unmark_hot(modeladmin, request, queryset):
    queryset.update(is_hot=False)


@admin.action(description='Mark selected products as new')
def mark_new(modeladmin, request, queryset):
    queryset.update(is_new=True)


@admin.action(description='Remove new badge')
def unmark_new(modeladmin, request, queryset):
    queryset.update(is_new=False)


@admin.action(description='Mark selected products as sold out')
def mark_sold_out(modeladmin, request, queryset):
    queryset.update(status='Sold Out', is_active=False)


@admin.action(description='Mark selected products as available')
def mark_available(modeladmin, request, queryset):
    queryset.update(status='Available', is_active=True)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'cover_preview',
        'title',
        'category',
        'price',
        'status',
        'server',
        'is_featured',
        'is_hot',
        'is_new',
        'is_active',
        'sort_order',
    )
    list_filter = ('category', 'status', 'server', 'is_featured', 'is_hot', 'is_new', 'is_active')
    search_fields = ('title', 'summary', 'category__name', 'server', 'account_level')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'status', 'is_featured', 'is_hot', 'is_new', 'is_active', 'sort_order')
    autocomplete_fields = ('category',)
    readonly_fields = ('large_cover_preview', 'created_at', 'updated_at')
    actions = (
        publish_items,
        unpublish_items,
        mark_featured,
        unmark_featured,
        mark_hot,
        unmark_hot,
        mark_new,
        unmark_new,
        mark_sold_out,
        mark_available,
    )
    fieldsets = (
        ('Product', {'fields': ('category', 'title', 'slug', 'summary')}),
        ('Account Details', {'fields': ('price', 'status', 'stock_note', 'server', 'account_level', 'delivery_note')}),
        ('Frontend Cover', {'fields': ('cover_image', 'image_url', 'large_cover_preview')}),
        ('Publishing', {'fields': ('is_featured', 'is_hot', 'is_new', 'is_active', 'sort_order')}),
        ('Dates', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Cover')
    def cover_preview(self, obj):
        return image_preview(obj.cover_image, obj.image_url)

    @admin.display(description='Cover preview')
    def large_cover_preview(self, obj):
        return image_preview(obj.cover_image, obj.image_url, 220)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'title', 'headline', 'support_hours', 'whatsapp_number', 'updated_at')
    readonly_fields = ('large_cover_preview', 'updated_at')
    fieldsets = (
        ('Brand', {'fields': ('store_name', 'announcement')}),
        ('Home Banner', {'fields': ('title', 'headline', 'description', 'cover_image', 'image_url', 'large_cover_preview')}),
        ('Contact', {'fields': ('whatsapp_number', 'support_hours')}),
        ('Updated', {'fields': ('updated_at',)}),
    )

    @admin.display(description='Cover preview')
    def large_cover_preview(self, obj):
        return image_preview(obj.cover_image, obj.image_url, 260)

    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)
