from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, SiteSetting

admin.site.site_header = 'Gameslot Store Administration'
admin.site.site_title = 'Gameslot Admin'
admin.site.index_title = 'Store Management'


def image_preview(image, size=54):
    if not image:
        return '-'
    return format_html(
        '<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:6px;" />',
        image.url,
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
    list_display = ('cover_preview', 'name', 'slug', 'badge', 'product_count', 'is_active', 'sort_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'badge', 'subtitle')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'sort_order')
    readonly_fields = ('large_cover_preview', 'created_at', 'updated_at')
    actions = (publish_items, unpublish_items)
    fieldsets = (
        ('Category', {'fields': ('name', 'slug', 'badge', 'subtitle', 'description')}),
        ('Frontend Cover', {'fields': ('cover_image', 'large_cover_preview')}),
        ('Publishing', {'fields': ('is_active', 'sort_order')}),
        ('Dates', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Cover')
    def cover_preview(self, obj):
        return image_preview(obj.cover_image)

    @admin.display(description='Cover preview')
    def large_cover_preview(self, obj):
        return image_preview(obj.cover_image, 220)

    @admin.display(description='Listings')
    def product_count(self, obj):
        return obj.products.count()


@admin.action(description='Mark selected products as featured')
def mark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)


@admin.action(description='Remove selected products from featured')
def unmark_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)


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
        'is_active',
        'sort_order',
    )
    list_filter = ('category', 'status', 'server', 'is_featured', 'is_active')
    search_fields = ('title', 'summary', 'category__name', 'server', 'account_level')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'status', 'is_featured', 'is_active', 'sort_order')
    autocomplete_fields = ('category',)
    readonly_fields = ('large_cover_preview', 'created_at', 'updated_at')
    actions = (publish_items, unpublish_items, mark_featured, unmark_featured)
    fieldsets = (
        ('Product', {'fields': ('category', 'title', 'slug', 'summary')}),
        ('Account Details', {'fields': ('price', 'status', 'server', 'account_level', 'delivery_note')}),
        ('Frontend Cover', {'fields': ('cover_image', 'large_cover_preview')}),
        ('Publishing', {'fields': ('is_featured', 'is_active', 'sort_order')}),
        ('Dates', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Cover')
    def cover_preview(self, obj):
        return image_preview(obj.cover_image)

    @admin.display(description='Cover preview')
    def large_cover_preview(self, obj):
        return image_preview(obj.cover_image, 220)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'title', 'headline', 'whatsapp_number', 'updated_at')
    readonly_fields = ('large_cover_preview', 'updated_at')
    fieldsets = (
        ('Brand', {'fields': ('store_name', 'announcement')}),
        ('Home Banner', {'fields': ('title', 'headline', 'description', 'cover_image', 'large_cover_preview')}),
        ('Contact', {'fields': ('whatsapp_number',)}),
        ('Updated', {'fields': ('updated_at',)}),
    )

    @admin.display(description='Cover preview')
    def large_cover_preview(self, obj):
        return image_preview(obj.cover_image, 260)

    def has_add_permission(self, request):
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)
