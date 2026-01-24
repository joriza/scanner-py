# Stock Scanner Pro

Aplicación web para escaneo y análisis básico de precios e indicadores técnicos (RSI, MACD) sobre series históricas. Optimizada para uso local con Flask y una base de datos SQLite para evitar descargas repetitivas.

## Descripción
Stock Scanner Pro permite:
- Actualizar precios de forma incremental (por ejemplo desde Yahoo Finance).
- Calcular indicadores RSI y MACD al vuelo.
- Detectar señales como RSI sobrevendido (RSI < 30) y oportunidades de MACD.
- Administración de tickers (alta/baja/limpieza de historial).

## Requisitos
- Python 3.8+
- Entorno virtual (recomendado)
- Dependencias listadas en requirements.txt

## Instalación y ejecución
1. Clona el repositorio y sitúate en la carpeta del proyecto:
   ```powershell
   cd c:\Users\USER\Desarrollo\scanner-py
   ```
2. Crea y activa un entorno virtual:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instala dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
4. Inicia la aplicación:
   ```powershell
   python -m flask run --port=5000
   ```
5. Abre el navegador en: http://127.0.0.1:5000

## Estructura principal
- app.py — Entrada de la aplicación Flask.
- database.py — Gestión y acceso a la base de datos SQLite.
- instance/scanner.db — Base de datos local con precios.
- templates/ — Plantillas HTML (dashboard, admin).
- static/ — Archivos estáticos (CSS).
- requirements.txt — Dependencias Python.

## Notas técnicas
- La base de datos local evita descargas redundantes y acelera operaciones.
- Los indicadores se calculan en tiempo de consulta para garantizar fórmulas actualizadas.
- Optimizada para temporalidad diaria en la Etapa 1.
- Normalización automática de símbolos (ej.: `BRK.B` → `BRK-B`).

## Operaciones comunes
- Agregar ticker: usar la interfaz de administración.
- Eliminar ticker: desde ABM se puede borrar y limpiar su historial.
- Forzar actualización de precios: operación disponible en el dashboard.

## Desarrollo y pruebas
- Mantener el entorno virtual activo durante desarrollo.
- Ejecutar linters/tests si los agrega el proyecto.
- Base de datos de desarrollo: instance/scanner.db (realizar backup antes de manipular).

## GitHub
- GitHub detecta automáticamente `readme.md` (nombre en minúsculas recomendado). Ya existe `LEEME.md`; puedo eliminarlo si lo desea después de confirmar.

## Contribución
- Abra un issue para sugerencias o reportes.
- Realice PRs siguiendo buenas prácticas y describiendo cambios.

## Licencia
- Indique aquí la licencia del proyecto (si aplica). Si no hay, por favor agregue una licencia para dejar explícito el uso permitido.

## Notas adicionales
- Se agregó *.pdf a .gitignore para evitar incluir documentos PDF en el repositorio.
- Mantenga backups de instance/scanner.db antes de realizar cambios masivos.