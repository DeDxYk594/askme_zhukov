from waitress import serve
from askme import wsgi

if __name__ == "__main__":
    serve(wsgi.application, host='0.0.0.0', port=8080)
