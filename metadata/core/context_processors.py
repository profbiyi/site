from django.conf import settings
from metadata.models import Link, Website


def links(request):
    queryset = Link.objects.distinct('name')
    return {
        'links': dict(zip(
            queryset.values_list('name', flat=True),
            queryset.values_list('url', flat=True)
        ))
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
