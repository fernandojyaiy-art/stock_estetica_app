# Stock Estética App

Aplicación web desarrollada con FastAPI para la gestión de stock y ventas de productos de estética.

## 🚀 Funcionalidades

- Gestión de productos (alta, stock, precios)
- Búsqueda de productos
- Control de bajo stock
- Registro de ventas
- Cálculo de valor total del inventario
- Cálculo de ganancia basado en precio de costo

## 🧱 Tecnologías

- Python
- FastAPI
- SQLite
- Jinja2 (templates HTML)

## 📁 Estructura del proyecto

stock_estetica_app/

main.py → rutas principales  
data_base.py → acceso a datos  
logic.py → lógica de negocio  
models.py → (en desarrollo)  
templates/ → vistas HTML  
cremas.db → base de datos local (ignorada en git)

## ⚙️ Instalación

```bash
git clone https://github.com/fernandojyaiy-art/stock_estetica_app.git
cd stock_estetica_app
pip install -r requirements.txt
uvicorn main:app --reload
