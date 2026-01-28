# Stock Scanner Pro

Aplicación web para escaneo y análisis de precios e indicadores técnicos sobre series históricas. Optimizada para uso local con Flask y una base de datos SQLite para evitar descargas repetitivas.

## 🚀 Características

- **Gestión de Tickers**: Agregar, eliminar y monitorear tickers de acciones
- **Sincronización Incremental**: Actualización de precios desde Yahoo Finance sin duplicados
- **Análisis Técnico**: Cálculo de indicadores RSI, MACD y EMAs al vuelo
- **Múltiples Estrategias**: 
  - RSI + MACD
  - 3 EMAs (diaria y semanal)
- **API REST**: Endpoints para integración con otras aplicaciones
- **Dashboard Interactivo**: Interfaz web para visualizar señales y datos

## 📋 Requisitos

- Python 3.8+
- Entorno virtual (recomendado)
- Dependencias listadas en [`requirements.txt`](requirements.txt)

## 🛠️ Instalación y Ejecución

### 1. Clonar el Repositorio
```bash
git clone https://github.com/joriza/scanner-py.git
cd scanner-py
```

### 2. Crear y Activar Entorno Virtual
```powershell
# Windows
python -m venv venv


# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar la Aplicación
```bash
python app.py
```

### 4.1 Activar entorno virtual e iniciar aplicacion e windows.
```bash
.\venv\Scripts\activate
python app.py
```

### 5. Acceder a la Aplicación
Abre el navegador en: http://127.0.0.1:5000

## 📖 Uso

### Agregar un Ticker
1. Ve a la página de administración: http://127.0.0.1:5000/admin
2. Ingresa el símbolo del ticker (ej: TSLA)
3. Haz clic en "Agregar"

### Sincronizar Datos
1. Ve al dashboard principal
2. Haz clic en "Actualizar Datos"
3. Espera a que se complete la sincronización

### Ver Señales de Trading
1. Selecciona la estrategia deseada (RSI+MACD o 3 EMAs)
2. Haz clic en "Escanear"
3. Revisa las señales generadas

## 🔌 API REST

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/tickers` | GET | Obtener todos los tickers |
| `/api/tickers` | POST | Agregar un nuevo ticker |
| `/api/tickers/<id>` | DELETE | Eliminar un ticker |
| `/api/refresh` | POST | Sincronizar datos de tickers |
| `/api/scan` | GET | Escanear tickers y obtener señales |

### Ejemplo de Uso

```bash
# Obtener todos los tickers
curl http://127.0.0.1:5000/api/tickers

# Agregar un ticker
curl -X POST http://127.0.0.1:5000/api/tickers \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'

# Escanear con estrategia RSI+MACD
curl http://127.0.0.1:5000/api/scan?strategy=rsi_macd
```

## 📊 Estrategias de Trading

### RSI + MACD
- **RSI Oversold**: RSI < 30
- **RSI Bullish**: RSI cruza por encima de su SMA después de oversold
- **MACD Active**: MACD > Signal y MACD ≤ 0

### 3 EMAs
- **Diaria**: Precio > EMA4 > EMA9 > EMA18
- **Semanal**: Precio > EMA4 > EMA9 > EMA18 (resampleado a viernes)

## 📁 Estructura del Proyecto

```
scanner-py/
├── app.py                      # Aplicación Flask principal
├── database.py                  # Modelos y gestión de base de datos
├── finance_service.py           # Servicio de sincronización y análisis
├── requirements.txt             # Dependencias Python
├── instance/
│   └── scanner.db              # Base de datos SQLite
├── scripts/
│   ├── check_db.py             # Verificar estado de la base de datos
│   ├── delete_empty_tickers.py  # Eliminar tickers sin datos
│   └── sync_data.py            # Sincronización manual de datos
├── static/
│   └── style.css               # Estilos de la aplicación
├── templates/
│   ├── index.html              # Dashboard principal
│   └── admin.html              # Panel de administración
└── DOCUMENTACION.md            # Documentación técnica detallada
```

## 🔧 Scripts de Utilidad

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

## 📝 Notas Técnicas

- La base de datos local evita descargas redundantes y acelera operaciones
- Los indicadores se calculan en tiempo de consulta para garantizar fórmulas actualizadas
- Normalización automática de símbolos (ej: `BRK.B` → `BRK-K`)
- Sincronización incremental basada en fecha de última actualización
- Soporte para múltiples estrategias de trading

## 🚀 Despliegue

### Render
1. Conectar el repositorio a Render
2. Configurar las variables de entorno necesarias
3. Render desplegará automáticamente la aplicación

### Docker
```bash
docker build -t scanner-pro .
docker run -p 5000:5000 scanner-pro
```

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📚 Documentación

Para más detalles técnicos, consulta la [documentación completa](DOCUMENTACION.md).

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 🔗 Enlaces

- [GitHub Repository](https://github.com/joriza/scanner-py)
- [Documentación Técnica](DOCUMENTACION.md)
- [Issues](https://github.com/joriza/scanner-py/issues)
