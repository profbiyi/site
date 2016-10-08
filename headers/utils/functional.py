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
