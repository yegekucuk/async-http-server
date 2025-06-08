from const import *
import asyncio
import time

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

async def handle_client(reader, writer):
    try:
        # Gelen veriyi oku ve decode et
        data = await reader.read(1024)
        request = data.decode('utf-8')
        request_info = parse_http(request)
        print("****** Incoming request:\n", request)

        # İsteği parse et ve yanıt döndür
        if request_info["method"] == "GET":
            writer.write(HTML_RESPONSE)
        else:
            writer.write(METHOD_NOT_ALLOWED)
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
        print("Sunucu manuel olarak durduruldu.")
