from const import *

def parse_http(http:str):
    # Satırları ayır
    lines = http.split("\r\n")
    if len(lines) == 0:
        return None
    
    # İlk satırı al (Request-Line)
    request_line = lines[0]
    parts = request_line.split()
    
    # Geçersiz format
    if len(parts) != 3:
        return None
    
    method, path, version = parts
    return {
        "method": method,
        "path": path,
        "version": version
    }

def generate_response(status_code: int,
                      headers: dict | None = None,
                      body: bytes | str = b"") -> bytes:
    """
    - status_code: HTTP status kodu (örn. 200)
    - headers: { "Content-Type": "text/html", ... }
    - body: bytes ya da str; str verilirse utf-8 ile encode edilir.

    Dönen değer: Tam HTTP/1.1 yanıtı (bytes).
    """
    # Status line
    reason = STATUS_MESSAGES.get(status_code, "")
    status_line = f"HTTP/1.1 {status_code} {reason}\r\n"

    # Body’yı bytes’a çevir
    if isinstance(body, str):
        body = body.encode("utf-8")

    # Eğer headers None ise boş dict yap
    if headers is None:
        headers = {}
    else:
        # Kendi dict’in bozulmaması için kopyala
        headers = headers.copy()

    # Zorunlu Content-Length header’ını ekle
    headers = headers.copy()
    headers.setdefault("Content-Length", str(len(body)))

    # Header satırlarını oluştur
    header_lines = ""
    for name, value in headers.items():
        header_lines += f"{name}: {value}\r\n"

    # İki boş satırdan sonra body gelir
    response = status_line + header_lines + "\r\n"
    return response.encode("utf-8") + body
