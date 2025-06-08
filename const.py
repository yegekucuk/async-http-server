# HOST ve PORT bilgileri
HOST = '127.0.0.1'
PORT = 9000

# Basit HTML içerik
HTML_RESPONSE = """\
<!DOCTYPE html>
<html>
<head><title>HTTP Server</title></head>
<body>
<h1>Welcome to the HTTP Server of Yunus Ege Kucuk!</h1>
</body>
</html>
"""
HTML_RESPONSE = HTML_RESPONSE.encode('utf-8')

# HTTP durum kodları
STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}