from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi import Query
from data_base import buscar_cremas
from data_base import actualizar_crema
from logic import calcular_valor_total
from data_base import registrar_venta
from data_base import obtener_ventas
from data_base import calcular_ganancia_total
from data_base import procesar_ventas_con_ganancia

from data_base import (
    crear_base_de_datos,
    obtener_cremas,
    insertar_crema,
    actualizar_stock,
    eliminar_crema,
    restar_stock,
    crear_tabla_ventas, 
    registrar_venta      

)

from logic import evaluar_stock, productos_bajo_stock

app = FastAPI()

templates = Jinja2Templates(directory="templates")



@app.on_event("startup")
def startup():
    crear_base_de_datos()
    crear_tabla_ventas()  # 👈 AGREGAR


@app.get("/")
def home(request: Request, busqueda: str = Query(None)):
    
    if busqueda:
        cremas = buscar_cremas(busqueda)
    else:
        cremas = obtener_cremas()

    mensaje = evaluar_stock(cremas)
    bajo_stock = productos_bajo_stock(cremas)

    total = calcular_valor_total(cremas)
    ganancia = calcular_ganancia_total()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cremas": cremas,
            "mensaje": mensaje,
            "bajo_stock": bajo_stock,
            "total": total,
            "ganancia": ganancia
        }
    )


@app.post("/crear")
def crear_crema(
    nombre: str = Form(...),
    descripcion: str = Form(""),
    cantidad: int = Form(...),
    precio: float = Form(...),
    precio_costo: float = Form(...)
):
    if cantidad < 0 or precio < 0 or precio_costo < 0:
        return RedirectResponse(url="/", status_code=303)

    insertar_crema(nombre, descripcion, cantidad, precio, precio_costo)
    return RedirectResponse(url="/", status_code=303)

@app.post("/sumar_stock")
def sumar_stock(
    id: int = Form(...),
    cantidad: int = Form(...)
):
    if cantidad <= 0:
        return RedirectResponse(url="/", status_code=303)

    actualizar_stock(id, cantidad)
    return RedirectResponse(url="/", status_code=303)


@app.post("/restar_stock")
def restar_stock_endpoint(
    id: int = Form(...),
    cantidad: int = Form(...)
):
    if cantidad <= 0:
        return RedirectResponse(url="/", status_code=303)

    try:
        restar_stock(id, cantidad)
    except ValueError:
        # Podés después mostrar mensaje si querés
        pass

    return RedirectResponse(url="/", status_code=303)

@app.post("/editar")
def editar_crema(
    id: int = Form(...),
    descripcion: str = Form(""),
    precio: float = Form(...)
):
    if precio < 0:
        return RedirectResponse(url="/", status_code=303)

    actualizar_crema(id, descripcion, precio)
    return RedirectResponse(url="/", status_code=303)

@app.post("/eliminar")
def eliminar(id: int = Form(...)):
    eliminar_crema(id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/vender")
def vender(
    id: int = Form(...),
    cantidad: int = Form(...)
):
    if cantidad <= 0:
        return RedirectResponse(url="/", status_code=303)

    try:
        registrar_venta(id, cantidad)
    except ValueError:
        pass

    return RedirectResponse(url="/", status_code=303)

@app.get("/ventas")
def ver_ventas(request: Request):

    ventas_raw = obtener_ventas()
    ventas = procesar_ventas_con_ganancia(ventas_raw)

    total_ganancia = sum(v["ganancia"] for v in ventas)
    total_ventas = sum(v["cantidad"] for v in ventas)

    return templates.TemplateResponse(
        "ventas.html",
        {
            "request": request,
            "ventas": ventas,
            "total_ganancia": total_ganancia,
            "total_ventas": total_ventas
        }
    )

