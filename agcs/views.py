from django import http
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.utils import six

ERR_CODES = {
    404: 'Page not found',
    500: 'Internal server error',
    403: 'Permission denied',
    400: 'Bad request',
}

class ErrorPage(object):
    def __init__(self, request, exception, code):
        self.code = code
        exception_repr = exception.__class__.__name__
        try:
            message = exception.args[0]
        except (AttributeError, IndexError):
            pass
        else:
            if isinstance(message, six.text_type):
                exception_repr = message
        self.context = {
            'request_path': getattr(request, 'path', None),
            'exception'   : exception_repr,
            'error_code'  : self.code,
            'error_text'  : ERR_CODES[self.code],
        }

        try:
            self.template = loader.get_template('errors/base_error.html')
            self.body = self.template.render(self.context, request)
            self.content_type = None             # Django will use DEFAULT_CONTENT_TYPE
        except TemplateDoesNotExist:
            self.template = Engine().from_string(
                '<h1>Not Found</h1>'
                '<p>The requested URL {{ request_path }} was not found on this server.</p>')
            self.body = self.template.render(Context(self.context))
            self.content_type = 'text/html'

    def get_response(self):
        if self.code == 404:
            return http.HttpResponseNotFound(self.body, content_type=self.content_type)
        elif self.code == 500:
            return http.HttpResponseServerError(self.body, content_type=self.content_type)
        elif self.code == 403:
            return http.HttpResponseForbidden(self.body, content_type=self.content_type)
        elif self.code == 400:
            return http.HttpResponseBadRequest(self.body, content_type=self.content_type)


#@cache_page(settings.DEBUG and 5 or 86400)
def page_not_found_view(request, exception):
    return ErrorPage(request, exception, 404).get_response()

#@cache_page(settings.DEBUG and 5 or 86400)
def server_error_view(request, exception):
    return ErrorPage(request, exception, 500).get_response()

#@cache_page(settings.DEBUG and 5 or 86400)
def permission_denied_view(request, exception):
    return ErrorPage(request, exception, 403).get_response()

#@cache_page(settings.DEBUG and 5 or 86400)
def bad_request_view(request, exception):
    return ErrorPage(request, exception, 400).get_response()
