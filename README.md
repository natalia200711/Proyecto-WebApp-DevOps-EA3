# Proyecto Web App DevOps — Evidencia de Aprendizaje 3 (EA3)

## Introducción
Aplicación web desarrollada en Python con Flask vinculada al caso de estudio de web scraping sobre el producto de Amazon (`ASIN: B0HFMCH32K`), integrando control de versiones en Git/GitHub, pruebas automatizadas con `pytest` y un pipeline de Integración Continua y Entrega Continua (CI/CD) en GitHub Actions.

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/natalia200711/Proyecto-WebApp-DevOps-EA3.git](https://github.com/natalia200711/Proyecto-WebApp-DevOps-EA3.git)
   cd Proyecto-WebApp-DevOps-EA3
   ```

2. Crear y activar el entorno virtual, e instalar dependencias:
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

## Uso
- Ejecutar la aplicación web de forma local:
  ```bash
  python app.py
  ```

- Ejecutar las pruebas automatizadas:
  ```bash
  pytest -v
  ```

## Automatización (CI/CD)
El flujo configurado en `.github/workflows/ci-cd.yml` se ejecuta automáticamente en cada `push` o `pull_request` hacia la rama `main`. Sus etapas son:
1. Clonar el código fuente en una máquina virtual limpia con `ubuntu-latest`.
2. Configurar Python 3.11.
3. Instalar las dependencias definidas en `requirements.txt`.
4. Ejecutar las pruebas unitarias e integración mediante `pytest -v`.
5. Validar la correcta importación de `app.py` para confirmar que está lista para despliegue.

## Despliegue en la Nube
- **Plataforma:** Render (Web Service)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **URL pública:** `https://proyecto-webapp-devops-ea3.onrender.com/`