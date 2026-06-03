from django.conf import settings

def site_config(request):
    """Global context processor for site configuration"""
    return {
        'SITE_NAME': 'BrandHostest',
        'SITE_DESCRIPTION': 'Your premium domain and hosting reseller platform',
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }
