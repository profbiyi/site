import json
from django.conf import settings

def extra(request):
    try:
        with settings.BASE_DIR.joinpath('context.json').open() as handle:
            return {'extra': json.load(handle)}
    except IOError: # pragma: no cover
        return {'extra': dict()}
