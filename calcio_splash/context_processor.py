from django.conf import settings


def global_setting(request):
    return {
        'MODE_TOURNAMENT': settings.WEBSITE_MODE == 'tournament',
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }
