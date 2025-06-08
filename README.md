# Async Python HTTP Server

Bu proje, Python'un `asyncio` kütüphanesini kullanarak geliştirilen hafif bir HTTP sunucusudur. Statik dosyaları sunabilir, API uç noktası sağlayabilir ve MIME tipi desteği sunar.

## 🔧 Özellikler

Kendi yazdığım bir HTTP sunucusu uygulamasıdır. 
Uygulama şu özellikleri desteklemektedir:
- TCP socket üzerinden `GET` istekleri
- `/static` dizininden dosya sunumu
- `/api/hello` endpoint’inden JSON döndürme
- MIME type yönetimi
- Çoklu bağlantı desteği (async)
- 404 ve 500 gibi HTTP hata yanıtlarını dönebilme

## 🚀 Kurulum ve Çalıştırma

1. Projeyi klonlayın:

```bash
git clone https://github.com/yegekucuk/async-http-server.git
cd async-http-server
```

2. Docker Compose ile başlatın:

```bash
docker-compose up --build
```

3. Tarayıcıdan erişin:

- Ana Sayfa: [http://localhost:8080/](http://localhost:8080/)
- Statik dosyalar (index.html, style.css): [http://localhost:8080/static/style.css](http://localhost:8080/static/style.css)
- API: [http://localhost:8080/api/hello](http://localhost:8080/api/hello)

## 📝 Lisans

Bu proje MIT lisansı ile lisanslanmıştır.
