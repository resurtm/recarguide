from django.conf import settings


def stripe_settings(request):
    return {'STRIPE_PUBLISHABLE_KEY': settings.STRIPE['PUBLISHABLE_KEY']}
