from app import app, consultar_producto

def test_ruta_health():
    cliente = app.test_client()
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.get_json()["status"] == "ok"

def test_estructura_consulta():
    datos = consultar_producto()
    assert datos["asin"] == "B0HFMCH32K"
    assert "tiempo" in datos