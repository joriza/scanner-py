# Scanner Pro Python - Documentación Técnica

## Descripción del Proyecto

Scanner Pro Python es una aplicación web para el análisis de señales de trading en tiempo real. Permite a los usuarios monitorear tickers de acciones, sincronizar datos históricos desde Yahoo Finance y generar señales de trading basadas en diferentes estrategias técnicas.

## Características Principales

- **Gestión de Tickers**: Agregar, eliminar y monitorear tickers de acciones
- **Sincronización de Datos**: Descarga automática de datos históricos desde Yahoo Finance
- **Análisis Técnico**: Generación de señales de trading usando indicadores técnicos
- **Interfaz Web**: Dashboard interactivo para visualizar señales y datos
- **API REST**: Endpoints para integración con otras aplicaciones

## Arquitectura del Sistema

### Componentes Principales

1. **Aplicación Flask** ([`app.py`](app.py))
   - Servidor web y API REST
   - Rutas para gestión de tickers y análisis
   - Integración con Swagger para documentación de API

2. **Servicio Financiero** ([`finance_service.py`](finance_service.py))
   - Sincronización de datos desde Yahoo Finance
   - Cálculo de indicadores técnicos (RSI, MACD, EMAs)
   - Normalización de símbolos de tickers

3. **Base de Datos** ([`database.py`](database.py))
   - Modelos de datos para Ticker y Price
   - Inicialización de base de datos SQLite
   - Restricciones de unicidad para evitar duplicados

4. **Scripts de Utilidad**
   - [`scripts/check_db.py`](scripts/check_db.py): Verificación del estado de la base de datos
   - [`scripts/delete_empty_tickers.py`](scripts/delete_empty_tickers.py): Eliminación de tickers sin datos
   - [`scripts/sync_data.py`](scripts/sync_data.py): Sincronización manual de datos

## Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el Repositorio**
   ```bash
   git clone https://github.com/joriza/scanner-py.git
   cd scanner-py
   ```

2. **Crear Entorno Virtual**
   ```bash
   python -m venv venv
   # En Windows
   venv\Scripts\activate
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instalar Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializar la Base de Datos**
   La base de datos se inicializa automáticamente al ejecutar la aplicación.

### Configuración

El proyecto puede configurarse mediante variables de entorno:

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URI de conexión a la base de datos | `sqlite:///instance/scanner.db` |
| `HOST` | Host del servidor Flask | `0.0.0.0` |
| `PORT` | Puerto del servidor Flask | `5000` |
| `FLASK_DEBUG` | Modo de depuración | `0` |

## Uso

### Ejecutar el Servidor de Desarrollo

```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`.

### API REST

#### Obtener Todos los Tickers
```http
GET /api/tickers
```

#### Agregar un Nuevo Ticker
```http
POST /api/tickers
Content-Type: application/json

{
  "symbol": "TSLA"
}
```

#### Eliminar un Ticker
```http
DELETE /api/tickers/<ticker_id>
```

#### Sincronizar Datos de Tickers
```http
POST /api/refresh
```

#### Escanear Tickers y Obtener Señales
```http
GET /api/scan?strategy=rsi_macd
```

Estrategias disponibles:
- `rsi_macd`: Señales basadas en RSI y MACD
- `3_emas`: Señales basadas en 3 EMAs (4, 9, 18)

## Estrategias de Trading

### Estrategia RSI + MACD

**Indicadores:**
- RSI (Relative Strength Index) con período 14
- MACD (12, 26, 9)

**Señales:**
- **RSI Oversold**: RSI < 30
- **RSI Bullish**: RSI cruza por encima de su SMA después de oversold
- **MACD Active**: MACD > Signal y MACD ≤ 0

### Estrategia 3 EMAs

**Indicadores:**
- EMA 4 (diaria)
- EMA 9 (diaria)
- EMA 18 (diaria)
- EMA 4 (semanal)
- EMA 9 (semanal)
- EMA 18 (semanal)

**Señales:**
- **Diaria**: Precio > EMA4 > EMA9 > EMA18
- **Semanal**: Precio > EMA4 > EMA9 > EMA18 (resampleado a viernes)

## Base de Datos

### Esquema

#### Tabla `ticker`
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | Integer | Identificador único |
| symbol | String(20) | Símbolo del ticker |
| name | String(100) | Nombre del ticker |
| sector | String(100) | Sector del ticker |
| is_active | Boolean | Estado del ticker |
| last_sync | DateTime | Última sincronización |

#### Tabla `price`
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | Integer | Identificador único |
| ticker_id | Integer | ID del ticker (FK) |
| date | Date | Fecha del precio |
| open | Float | Precio de apertura |
| high | Float | Precio máximo |
| low | Float | Precio mínimo |
| close | Float | Precio de cierre |
| volume | BigInteger | Volumen de operaciones |

**Restricción de Unicidad:** `(ticker_id, date)`

## Scripts de Utilidad

### Verificar Estado de la Base de Datos
```bash
python scripts/check_db.py
```

### Eliminar Tickers Sin Datos
```bash
python scripts/delete_empty_tickers.py
```

### Sincronizar Datos Manualmente
```bash
python scripts/sync_data.py
```

## Despliegue

### Render

1. Conectar el repositorio a Render
2. Configurar las variables de entorno necesarias
3. Render desplegará automáticamente la aplicación

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

## Contribución

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.

## Soporte

Para preguntas o problemas, por favor abre un issue en el repositorio de GitHub.
