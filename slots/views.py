from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product, SiteSetting


def image_url(request, image_field):
    if not image_field:
        return ''
    return request.build_absolute_uri(image_field.url)


def serialize_category(request, category):
    active_products = category.products.filter(is_active=True)
    return {
        'name': category.name,
        'slug': category.slug,
        'badge': category.badge,
        'subtitle': category.subtitle,
        'description': category.description,
        'coverImage': image_url(request, category.cover_image),
        'stock': active_products.count(),
    }


def serialize_product(request, product):
    return {
        'title': product.title,
        'slug': product.slug,
        'category': product.category.name,
        'categorySlug': product.category.slug,
        'price': product.price,
        'status': product.status,
        'server': product.server,
        'accountLevel': product.account_level,
        'summary': product.summary,
        'deliveryNote': product.delivery_note,
        'coverImage': image_url(request, product.cover_image) if product.cover_image else product.image_url,
    }


def frontend(request):
    return render(request, 'index.html')


def category_page(request, slug):
    return render(request, 'category/index.html')


def home_api(request):
    categories = Category.objects.filter(is_active=True).prefetch_related('products')
    products = (
        Product.objects.filter(is_active=True, is_featured=True)
        .select_related('category')
        .order_by('sort_order', '-created_at')[:8]
    )
    setting = SiteSetting.objects.first()

    return JsonResponse(
        {
            'site': {
                'storeName': setting.store_name if setting else 'Gameslot',
                'title': setting.title if setting else 'New Season Stock',
                'headline': setting.headline if setting else 'No Reroll, No Life',
                'description': setting.description
                if setting
                else 'Starter accounts, VIP collections, and reroll picks refreshed for anime game players.',
                'coverImage': image_url(request, setting.cover_image) if setting else '',
                'announcement': setting.announcement
                if setting
                else 'Fresh accounts are reviewed and updated regularly.',
                'whatsappNumber': setting.whatsapp_number if setting else '60102431634',
            },
            'categories': [serialize_category(request, category) for category in categories],
            'latestListings': [serialize_product(request, product) for product in products],
        }
    )


def category_api(request, slug):
    category = get_object_or_404(Category.objects.prefetch_related('products'), slug=slug, is_active=True)
    products = category.products.filter(is_active=True).select_related('category')
    setting = SiteSetting.objects.first()
    return JsonResponse(
        {
            'category': serialize_category(request, category),
            'products': [serialize_product(request, product) for product in products],
            'whatsappNumber': setting.whatsapp_number if setting else '60102431634',
        }
    )
