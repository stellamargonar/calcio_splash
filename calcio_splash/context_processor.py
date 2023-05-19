from django.conf import settings


def website_mode(request):
    return {'MODE_TOURNAMENT': settings.WEBSITE_MODE == 'tournament'}
