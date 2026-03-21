# 📦 Stock Estética App

Aplicación web para la gestión de stock de productos de estética, desarrollada con Python y FastAPI.

---

## 🚀 Descripción

Sistema simple pero funcional que permite administrar el inventario de productos, pensado para uso real en un entorno de negocio pequeño.

Incluye control de stock en tiempo real, permitiendo registrar tanto ingresos de mercadería como ventas.

---

## 🛠️ Funcionalidades

* ✔ Alta de productos
* ✔ Visualización de stock
* ✔ Sumar stock (ingreso de mercadería)
* ✔ Restar stock (ventas)
* ✔ Eliminación de productos
* ✔ Validación para evitar stock negativo
* ✔ Alertas de stock bajo
* ✔ Mensajes dinámicos según estado del inventario

---

## 🧱 Tecnologías utilizadas

* Python 3
* FastAPI
* SQLite
* Jinja2

---

## 📂 Estructura del proyecto

```id="9slw0u"
stock_estetica_app/
│
├── main.py            # Rutas y flujo principal
├── data_base.py       # Acceso a datos (SQLite)
├── logic.py           # Lógica de negocio
├── models.py          # (pendiente para futuras mejoras)
├── templates/
│   └── index.html     # Interfaz de usuario
└── cremas.db          # Base de datos local (no versionada)
```

---

## ⚙️ Instalación y ejecución

1. Clonar el repositorio:

```bash id="b7axv9"
git clone https://github.com/tu-usuario/stock_estetica_app.git
cd stock_estetica_app
```

2. Instalar dependencias:

```bash id="kczs9u"
pip install fastapi uvicorn jinja2
```

3. Ejecutar el servidor:

```bash id="0qz5c6"
uvicorn main:app --reload
```

4. Acceder desde el navegador:

```id="u4dfmb"
http://127.0.0.1:8000
```

---

## 📱 Uso desde celular

Se puede acceder desde un celular dentro de la misma red local ejecutando:

```bash id="4r8r2y"
uvicorn main:app --host 0.0.0.0 --reload
```

Y accediendo a la IP local desde el navegador del dispositivo.

---

## 📌 Estado del proyecto

🔹 Fase 1 completada

* CRUD completo implementado
* Lógica de negocio separada en `logic.py`
* Aplicación funcional para uso real

---

## 🔜 Próximas mejoras (Fase 2)

* Implementación de modelos (`models.py`)
* Validaciones más robustas
* Prevención de productos duplicados
* Mejora de interfaz (UI/UX)
* Deploy en servidor para acceso remoto
* Integración con sistema de turnos

---

## 🧠 Objetivo del proyecto

Este proyecto forma parte de un proceso de aprendizaje enfocado en desarrollo backend, aplicando buenas prácticas de arquitectura y evolución progresiva de un producto real.

---

## 👨‍💻 Autor

Mati
