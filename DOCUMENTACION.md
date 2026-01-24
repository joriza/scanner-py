# Documentación del Proyecto: Stock Scanner Pro

Este documento detalla la arquitectura, procesos de inicio y la lógica implementada para el rastreador de acciones basado en indicadores técnicos.

## 1. Instrucciones de Inicio

### Inicio por Primera Vez (Instalación)
Si estás en una carpeta nueva o es la primera vez que clonas el proyecto:
1.  **Crear entorno virtual**: `python -m venv venv`
2.  **Activar entorno**: `.\venv\Scripts\activate`
3.  **Instalar dependencias**: `pip install flask flask-sqlalchemy yfinance pandas pandas-ta`
4.  **Inicializar Base de Datos**: Ejecuta la aplicación; las tablas se crearán automáticamente.
5.  **Cargar Tickers Iniciales**: Ve a la pestaña "Administración" y haz clic en "Cargar Tickers de Ejemplo".

### Inicio de Rutina (Siguientes Veces)
Para sesiones normales de uso, **no es necesario reinstalar nada**:
1.  Abre la terminal en la carpeta del proyecto.
2.  Activa el entorno: `.\venv\Scripts\activate`
3.  Inicia el servidor: `python -m flask run --port=5000`

---

## 2. Descripción Operativa
La aplicación funciona mediante un **backend en Flask (Python)** y una **interfaz web (HTML/JS/CSS)**. Los datos son provistos por Yahoo Finance de forma gratuita.

### Arquitectura de Datos
*   **Persistentencia**: Se utiliza **SQLite** (`scanner.db`) para guardar:
    *   Listado de tickers a seguir.
    *   Historial de precios (OHLCV) diario de cada ticker.
*   **Sincronización Incremental**: La app no descarga todo el historial cada vez. Solo descarga los datos desde la última fecha guardada en la base de datos hasta hoy, optimizando velocidad y consumo de datos.

---

## 3. Lógica de Indicadores (Etapa 1 - Diaria)
Los indicadores se calculan "en memoria" al momento de abrir el Dashboard para asegurar flexibilidad.

### Estrategias Implementadas:

#### 1-RSI+MACD
1.  **RSI < 30 (1 año)**: Fecha y días desde la última sobreventa severa.
2.  **Tendencia RSI (Rebote)**: Primer cruce alcista de RSI sobre su SMA post-sobreventa.
3.  **Oportunidad MACD**: Cruce alcista bajo cero (12, 26, 9).

#### 2-3_EMAS
1.  **Precio > 3 EMAS**: Detecta cuando el **Precio de Cierre** se posiciona simultáneamente por encima de las Medias Móviles Exponenciales (EMA) de **5, 9 y 20 períodos**.
2.  **Visualización**: Muestra la fecha en que se produjo la condición por última vez y hace cuántos días. Si el precio sigue por encima hoy, la señal aparece en **Verde**, de lo contrario en **Rojo**.

---

## 4. Selección de Estrategias
El Dashboard incluye un selector que permite cambiar entre estrategias. Al cambiar la opción:
*   La tabla se actualiza dinámicamente.
*   Los encabezados cambian para reflejar los indicadores pertinentes.
*   El ordenamiento se ajusta automáticamente (los eventos más recientes de cada estrategia aparecen primero).

---

## 4. Control de Versiones
El proyecto se gestiona con Git:
- **Rama master**: Versión estable Etapa 1.
- **Rama [Fecha ISO]**: Ramas de trabajo diario (ej. `2026-01-23`).

---

## 4. Estructura de Archivos
*   `app.py`: Servidor y rutas de la API.
*   `database.py`: Modelos de la base de datos.
*   `finance_service.py`: Lógica de descarga de datos y cálculos matemáticos.
*   `static/style.css`: Estética moderna y Modo Oscuro.
*   `templates/`: Interfaces visuales (Dashboard y Admin).
*   `venv/`: Entorno virtual de Python (aislado del sistema).

---

## 5. Mantenimiento (Etapa 2 - Planificado)
*   **Carga Masiva**: Implementada en la interfaz de Administración.
*   **Nuevas Temporalidades**: Próximamente Weekly y Hourly.
*   **Gráficos Interactivos**: Integración de Lightweight Charts.
