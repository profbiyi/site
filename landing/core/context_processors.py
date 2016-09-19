import json
from django.conf import settings

def extra(request):
    extra = {
       'favicon_prefix': settings.FAVICON_PREFIX
    } if getattr(settings, 'FAVICON_PREFIX', None) else {}

    try:
        with settings.BASE_DIR.joinpath('context.json').open() as handle:
            extra.update(json.load(handle))
    except IOError: # pragma: no cover
        pass

    return { 'extra': extra }

