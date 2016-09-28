from django.conf import settings
from metadata.models import Link, Website


def links(request):
    return {
        'links': {
            l.name: l.url for l in Link.objects.all()
        }
    }

def _website():
    try:
        return {
            'site': Website.objects.get(
                site__name=settings.DEFAULT_WEBSITE_NAME
            )
        }
    except (AttributeError, Website.DoesNotExist):
        return {
            'site': Website.objects.first()
        }

def website(request):
    return _website()
