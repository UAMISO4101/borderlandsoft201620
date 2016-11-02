from django.conf import settings


def admin_media(request):  # No borrar parámetro request
    return {
        'SOCIAL_AUTH_FACEBOOK_KEY': settings.SOCIAL_AUTH_FACEBOOK_KEY
    }
