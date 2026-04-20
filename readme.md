# 🧴 Stock Estética App

Aplicación web desarrollada con FastAPI para la gestión de stock, ventas y análisis de productos en un negocio de estética.

---

## 🚀 Funcionalidades

* 📦 Gestión de productos (cremas)
* 🔍 Búsqueda de productos
* ⚠️ Alertas de bajo stock
* 💰 Cálculo de valor total del inventario
* 📊 Cálculo de ganancia potencial (precio vs costo)
* 🛒 Registro de ventas
* 📈 Visualización de datos financieros

---

## 🛠️ Tecnologías

* Python 3
* FastAPI
* SQLite
* Jinja2 (templates HTML)

---

## 📂 Estructura del proyecto

stock_estetica_app/
├── main.py
├── data_base.py
├── logic.py
├── models.py (en desarrollo)
├── templates/
│   ├── index.html
│   └── ventas.html

---

## ⚙️ Instalación

1. Clonar el repositorio:

git clone https://github.com/fernandojyaiy-art/stock_estetica_app.git
cd stock_estetica_app

2. Crear entorno virtual:

python -m venv venv
venv\Scripts\activate

3. Instalar dependencias:

pip install -r requirements.txt

4. Ejecutar la app:

uvicorn main:app --reload

5. Abrir en navegador:

http://127.0.0.1:8000

---

## 📌 Notas

* La base de datos (cremas.db) no está versionada
* Proyecto en desarrollo activo 🚧

---

## 👨‍💻 Autor

Matias Jyaiy
