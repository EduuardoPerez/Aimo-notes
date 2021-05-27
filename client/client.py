# Run with "python client.py"
from bottle import get, run, static_file

@get('/')
def index():
    return static_file('index.html', root=".")

@get('/:path#(src|images|css|js|fonts)\/.+#')
def server_static(path):
    return static_file(path, root='.')

run(host='localhost', port=5000)
