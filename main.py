from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from data_base import crear_base_de_datos
from data_base import obtener_cremas
from fastapi import Form
from fastapi.responses import RedirectResponse
from data_base import insertar_crema
from data_base import actualizar_stock
from data_base import eliminar_crema
from data_base import restar_stock
from logic import evaluar_stock, productos_bajo_stock

app = FastAPI()

templates = Jinja2Templates(directory="templates")



#aca tenemos que generar la base de datos de las cremas, cantidades y precios de cada una. con una simple descripcion de la misma. mas un codigo de id.#


crear_base_de_datos ()

#aca tenemos que generar la base de datos de las cremas, cantidades y precios de cada una. con una simple descripcion de la misma. mas un codigo de id.#


@app.get("/")
def home(request: Request):
    cremas = obtener_cremas()

    mensaje = None

    if len(cremas) == 0:
        mensaje = "No hay productos cargados. Agregá stock."
    elif len(cremas) == 1:
        mensaje = "Solo queda 1 producto. Revisar stock."

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cremas": cremas,
            "mensaje": mensaje
        }
    )

#aca tenemos que generar la base de datos de las cremas, cantidades y precios de cada una. con una simple descripcion de la misma. mas un codigo de id.#
@app.post("/crear")
def crear_crema(
    nombre: str = Form(...),
    descripcion: str = Form(""),
    cantidad: int = Form(...),
    precio: float = Form(...)
):
    insertar_crema(nombre, descripcion, cantidad, precio)

    return RedirectResponse(url="/", status_code=303)

#|aca tenemos que generar la base de datos de las cremas, cantidades y precios de cada una. con una simple descripcion de la misma. mas un codigo de id.#
@app.post("/sumar_stock")
def sumar_stock(
    id: int = Form(...),
    cantidad: int = Form(...)
):
     # 🔴 validación
    if cantidad <= 0:
        return RedirectResponse(url="/", status_code=303)

    actualizar_stock(id, cantidad)

    return RedirectResponse(url="/", status_code=303)

#aca tenemos que generar la base de datos de las cremas, cantidades y precios de cada una. con una simple descripcion de la misma. mas un codigo de id.#
@app.post("/eliminar")
def eliminar(id: int = Form(...)):
    eliminar_crema(id)
    return RedirectResponse(url="/", status_code=303)

#aca restamos por ventas o por mermas, lo que sea. con una simple descripcion de la misma. mas un codigo de id.#
@app.post("/restar_stock")
def restar_stock_endpoint(
    id: int = Form(...),
    cantidad: int = Form(...)
):
    # Validación básica
    if cantidad <= 0:
        return RedirectResponse(url="/", status_code=303)

    restar_stock(id, cantidad)

    return RedirectResponse(url="/", status_code=303)

#aca evaluamos stock y mostramos mensajes de alerta. con una simple descripcion de la misma. mas un codigo de id.#
@app.get("/")
def home(request: Request):
    cremas = obtener_cremas()

    mensaje = evaluar_stock(cremas)
    bajo_stock = productos_bajo_stock(cremas)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "cremas": cremas,
            "mensaje": mensaje,
            "bajo_stock": bajo_stock
        }
    )