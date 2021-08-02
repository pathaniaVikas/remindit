
"""
Test app to test if gunicorn is able to call this method.
Doc: https://docs.gunicorn.org/en/stable/run.html
"""


# app will be called by gunicorn
def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
