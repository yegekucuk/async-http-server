from const import *
import asyncio
import time
import os
import mimetypes

def parse_http(http:str):
    # Satırları ayır
    lines = http.split("\r\n")
    if len(lines) == 0:
        return None
    
    # İlk satırı al (Request-Line)
    request_line = lines[0]
    parts = request_line.split()
    
    if len(parts) != 3:
        return None  # Geçersiz format
    
    method, path, version = parts
    return {
        "method": method,
        "path": path,
        "version": version
    }

async def serve_static_file(path, writer):
    # path örn: /static/style.css
    file_path = path.lstrip("/")  # baştaki / karakterini kaldır
    if not os.path.isfile(file_path):
        # Dosya yoksa 404 gönder
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 Not Found".encode("utf-8")
        writer.write(response)
        return

    # Dosya varsa içeriğini oku
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        # MIME type belirle
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"
        # Yanıtı oluştur
        header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\n\r\n".encode("utf-8")
        writer.write(header + content)
    except Exception as e:
        print("Error while serving static file:", e)
        response = b"HTTP/1.1 500 Internal Server Error\r\n\r\nInternal Server Error"
        writer.write(response)

async def handle_client(reader, writer):
    try:
        # Gelen veriyi oku ve decode et
        data = await reader.read(1024)
        request = data.decode('utf-8')
        parsed = parse_http(request)
        # Parse edilemiyorsa 400 dön
        if not parsed:
            writer.write(b"HTTP/1.1 400 Bad Request\r\n\r\nBad Request")
            return
        print("****** Incoming request:\n", request)
        # İsteğin metodunu ve path'ini getir
        method = parsed["method"]
        path = parsed["path"]
        if method != "GET":
            # GET metodu değilse izin verme
            writer.write(b"HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed")
        elif path.startswith("/static/"):
            # Statikten dosyayı getir
            await serve_static_file(path, writer)
        elif path == "/":
            # Ana sayfa (HTML yanıt)
            writer.write(HTML_RESPONSE)
        elif path == "/api/hello":
            # API'den hello yanıtı dön
            response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"message\": \"Hello from the API!\"}"
            writer.write(response)
        else:
            writer.write(b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found")
        
        await writer.drain()
    except Exception as e:
        print("Error:", e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    # asyncio kütüphanesi ile async bir server oluştur
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"Async Server is on {HOST}:{PORT}")

    # Belirli bir süre çalıştıktan sonra sunucuyu kapat
    runtime = 60
    async with server:
        start_time = time.time()
        while time.time() - start_time < runtime:
            await asyncio.sleep(0.1)
        print(f"Server is up for {runtime} seconds. Shutting down the server.")
        server.close()
        await server.wait_closed()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server was stopped manually.")
