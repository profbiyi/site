import subprocess

def set_headers(response, default=True, **headers):
    for header,value in headers.items():
        if default:
            response.setdefault(header, value)
        else:
            response[header] = value


def del_headers(response, *headers):
    for header in headers:
        if response.has_header(header):
            del(response[header])


def get_uwsgi_version():
    status, output = subprocess.getstatusoutput(['uwsgi --version'])
    return None if status else output


def get_gunicorn_version(): # pragma: no cover
    try:
        from gunicorn import __version__
        return __version__
    except ImportError:
        return None
