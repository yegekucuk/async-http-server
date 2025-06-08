# HOST ve PORT bilgileri
HOST = '127.0.0.1'
PORT = 9000

# Basit HTML içerik
HTML_RESPONSE = """\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html>
<head><title>HTTP Server</title></head>
<body>
<h1>Welcome to the HTTP Server of Yunus Ege Kucuk!</h1>
</body>
</html>
"""
HTML_RESPONSE = HTML_RESPONSE.encode('utf-8')

# Şimdilik sadece GET destekleniyor
METHOD_NOT_ALLOWED = """\
HTTP/1.1 405 Method Not Allowed
Content-Type: text/plain
Connection: close

Only GET method is supported.
"""
METHOD_NOT_ALLOWED = METHOD_NOT_ALLOWED.encode('utf-8')