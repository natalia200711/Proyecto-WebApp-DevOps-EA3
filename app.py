import os
import time
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string

app = Flask(__name__)

ASIN = "B0HFMCH32K"
URL_PRODUCTO = f"https://www.amazon.com/dp/{ASIN}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Monitor DevOps - {{ asin }}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto; padding: 20px; background: #f4f6f9; color: #222; }
        .card { background: #fff; padding: 24px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
        .badge { display: inline-block; background: #e6f4ea; color: #137333; padding: 4px 10px; border-radius: 6px; font-weight: bold; }
        .meta { margin-top: 16px; line-height: 1.7; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">CI/CD Activo • EA3 DevOps</span>
        <h1>Aplicación Web de Monitoreo y Scraping</h1>
        <p><strong>Producto objetivo (EA1/EA2):</strong> Auriculares inalámbricos híbridos con cancelación activa de ruido Bluetooth (MMWOWARTS)</p>
        <div class="meta">
            <p><strong>ASIN:</strong> {{ asin }}</p>
            <p><strong>Estado de consulta:</strong> {{ estado }}</p>
            <p><strong>Título detectado:</strong> {{ titulo }}</p>
            <p><strong>Precio detectado:</strong> {{ precio }}</p>
            <p><strong>Tiempo de respuesta:</strong> {{ tiempo }} s</p>
        </div>
    </div>
</body>
</html>
"""

def consultar_producto():
    inicio = time.time()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }
    titulo = "No encontrado (protección anti-bot / captcha)"
    precio = "No disponible"
    estado = "Ejecución controlada (HTTP 200 / Resiliencia)"

    try:
        resp = requests.get(URL_PRODUCTO, headers=headers, timeout=12)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            title_el = soup.find("span", id="productTitle")
            price_el = soup.find("span", class_="a-offscreen")
            if title_el:
                titulo = title_el.get_text(strip=True)
            if price_el:
                precio = price_el.get_text(strip=True)
            estado = f"OK (HTTP {resp.status_code})"
        else:
            estado = f"Restringido / HTTP {resp.status_code}"
    except Exception as exc:
        estado = f"Controlado por excepción: {exc}"

    tiempo = round(time.time() - inicio, 4)
    return {"asin": ASIN, "titulo": titulo, "precio": precio, "estado": estado, "tiempo": tiempo}

@app.route("/")
def index():
    datos = consultar_producto()
    return render_template_string(HTML_TEMPLATE, **datos)

@app.route("/health")
def health():
    return {"status": "ok", "asin": ASIN}, 200

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto)