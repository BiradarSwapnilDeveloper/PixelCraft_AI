import urllib.request

urls = [
    'http://localhost:8080/index.html',
    'http://localhost:8080/blog',
    'http://localhost:8080/blog/',
    'http://localhost:8080/blog.html',
    'http://localhost:8080/blog/index.html',
    'http://localhost:8080/tools',
    'http://localhost:8080/tools/',
    'http://localhost:8080/tools/image-compressor',
    'http://localhost:8080/tools/image-compressor.html',
    'http://localhost:8080/about-us',
    'http://localhost:8080/about-us.html',
]

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers): return fp
    def http_error_302(self, req, fp, code, msg, headers): return fp

opener = urllib.request.build_opener(NoRedirect)

for u in urls:
    try:
        res = opener.open(u)
        loc = res.headers.get('Location', 'None')
        print(f'{u:50} -> Status: {res.status}  Loc: {loc}')
    except Exception as e:
        print(f'{u:50} -> Error: {e}')
