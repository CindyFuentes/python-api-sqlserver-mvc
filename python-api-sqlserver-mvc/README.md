# Atlántico Turístico
Aplicación web de consulta y gestión de atractivos turísticos del Atlántico con Python, Flask, SQL Server y API REST de datos.gov.co.

## Funcionalidades
- Consumo de API y procesamiento JSON.
- Importación/actualización de datos en SQL Server.
- Catálogos relacionales de municipios y tipos.
- Búsqueda de atractivos.
- CRUD de atractivos locales.
- CRUD de reseñas y calificaciones.
- Panel de indicadores.

> La API es una fuente pública de consulta. El sistema no modifica datos en datos.gov.co. Las reseñas son registros locales.

## Requisitos
Python 3.10+, SQL Server Express/Developer, Microsoft ODBC Driver 18 for SQL Server y Visual Studio Code.

## Instalación en Windows
1. Descomprime y abre esta carpeta en Visual Studio Code.
2. En la terminal integrada:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. En SSMS, ejecuta `database/script.sql` para crear la base `AtlanticoTuristico`.
4. Copia `.env.example` como `.env` y ajusta `SQL_SERVER` a tu instancia. Por defecto usa autenticación de Windows.
5. Ejecuta:
   ```powershell
   python app.py
   ```
6. Abre http://127.0.0.1:5000
7. Entra en Importar API y pulsa Consultar API e importar.

## Estructura
- `models/`: conexión y operaciones de datos.
- `services/`: consumo e importación de la API.
- `templates/`: páginas HTML.
- `static/`: estilos CSS.
- `database/`: script SQL.

## Campos de la fuente
Se esperan campos equivalentes a `municipio`, `tipo_de_atractivo`, `subregion`, `atractivo_turistico_o_producto`, `lugar_de_ubicacion`, `descripcion` y `:id`. Si el proveedor cambia la estructura JSON, ajustar `services/api.py`.

## Seguridad
No publiques `.env`, claves ni contraseñas. `FLASK_DEBUG` debe ser false en producción. Antes de desplegar en internet agrega autenticación, autorización, protección CSRF y endurecimiento de seguridad.

Proyecto académico y de portafolio de Cindy Carolina Fuentes González.
