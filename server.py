from const import *
from utils import *
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
    
    # Geçersiz format
    if len(parts) != 3:
        return None
    
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
        response = generate_response(
            400,
            {"Content-Type": "text/plain",
             "Connection": "close"},
            "File not found."
        )
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
        response = generate_response(
            200,
            {"Content-Type": mime_type},
            content
        )
        writer.write(response)
    except Exception as e:
        print("Error while serving static file:", e)
        response = generate_response(
            500,
            {"Content-Type": "text/plain",
             "Connection": "close"},
            "Internal Server Error"
        )
        writer.write(response)

async def handle_client(reader, writer):
    try:
        # Gelen veriyi oku ve decode et
        data = await reader.read(1024)
        request = data.decode('utf-8')
        parsed = parse_http(request)
        # Parse edilemiyorsa 400 dön
        if not parsed:
            writer.write(generate_response(
                400,
                {"Content-Type": "text/plain",
                "Connection": "close"},
                "Bad Request"
            ))
            return
        print("****** Incoming request:\n", request)
        # İsteğin metodunu ve path'ini getir
        method = parsed["method"]
        path = parsed["path"]
        if method != "GET":
            # GET metodu değilse izin verme
            writer.write(generate_response(
                405,
                {"Content-Type": "text/plain",
                "Connection": "close"},
                "Method Not Allowed"
            ))
        elif path.startswith("/static/"):
            # Statikten dosyayı getir
            await serve_static_file(path, writer)
        elif path == "/":
            # Ana sayfa (HTML yanıt)
            writer.write(generate_response(
                200,
                {"Content-Type": "text/html; charset=utf-8"},
                HTML_RESPONSE
            ))
        elif path == "/api/hello":
            # API'den hello yanıtı dön
            writer.write(generate_response(
                200,
                {"Content-Type": "application/json"},
                '{"message":"Hello from the API!"}'
            ))
        else:
            writer.write(generate_response(
                404,
                {"Content-Type": "text/plain",
                "Connection": "close"},
                "404 Not Found"
            ))
        
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
    runtime = 3600
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
