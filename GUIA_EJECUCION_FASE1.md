# Guía para Ejecutar Scanner Pro con Fase 1 Implementada

**Fecha:** 30 de enero de 2026
**Objetivo:** Ejecutar la aplicación con las mejoras de la Fase 1 implementadas

## 📋 Prerrequisitos

1. **Python 3.8+** instalado
2. **Entorno virtual** creado (opcional pero recomendado)
3. **Directorio del proyecto:** `c:/Users/USER/Desarrollo/scanner-py`

---

## 🚀 Paso 1: Activar Entorno Virtual

### Windows:
```bash
# Navegar al directorio del proyecto
cd c:/Users/USER/Desarrollo/scanner-py

# Crear entorno virtual (si no existe)
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

### macOS/Linux:
```bash
# Navegar al directorio del proyecto
cd /path/to/scanner-py

# Crear entorno virtual (si no existe)
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

**✅ Verificación:** Deberías ver `(venv)` al inicio de tu línea de comandos.

---

## 📦 Paso 2: Instalar Dependencias

```bash
# Instalar todas las dependencias (incluyendo las nuevas de Fase 1)
pip install -r requirements.txt
```

**⏱️ Tiempo estimado:** 2-5 minutos

**✅ Verificación:** Si no hay errores, todas las dependencias están instaladas.

---

## 🧪 Paso 3: Verificar Implementación (Opcional)

```bash
# Ejecutar script de verificación automática
python scripts/verify_fase1.py
```

Este script verificará:
- ✅ Todas las dependencias están instaladas
- ✅ Los módulos nuevos se importan correctamente
- ✅ [`app.py`](app.py) no tiene errores de sintaxis
- ✅ Los archivos de tests se compilan correctamente
- ✅ La configuración de pytest existe

---

## 🧪 Paso 4: Ejecutar Tests (Opcional)

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con verbosidad
pytest -v

# Ejecutar con reporte de cobertura
pytest --cov=. --cov-report=html
```

**📊 Para ver el reporte de cobertura:**
1. Abre el archivo `htmlcov/index.html` en tu navegador
2. Verifica que la cobertura sea ≥70%

---

## 🚀 Paso 5: Ejecutar la Aplicación

```bash
# Ejecutar en modo desarrollo
python app.py
```

**📝 Salida esperada:**
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

---

## 🔍 Paso 6: Verificar Endpoints

### 6.1 Health Check:

```bash
# En otra terminal
curl http://localhost:5000/health
```

**✅ Respuesta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T00:30:00.000Z",
  "checks": {
    "database": "ok",
    "cache": "ok"
  }
}
```

### 6.2 Métricas de Prometheus:

```bash
curl http://localhost:5000/metrics
```

**✅ Respuesta esperada:** Texto con métricas de Prometheus

### 6.3 API de Tickers:

```bash
# Obtener todos los tickers
curl http://localhost:5000/api/tickers

# Agregar un ticker
curl -X POST http://localhost:5000/api/tickers ^
  -H "Content-Type: application/json" ^
  -d "{\"symbol\": \"TSLA\"}"
```

### 6.4 Dashboard:

Abre tu navegador en: http://localhost:5000

---

## 🎯 Paso 7: Probar Funcionalidades

### 7.1 Agregar un Ticker:

1. Ve a http://localhost:5000/admin
2. Ingresa el símbolo (ej: `AAPL`)
3. Haz clic en "Agregar"
4. Verifica que aparece en la lista

### 7.2 Sincronizar Datos:

1. Ve a http://localhost:5000
2. Haz clic en "Actualizar Precios"
3. Espera a que se complete la sincronización
4. Verifica los logs en la terminal

### 7.3 Escanear Señales:

1. Selecciona una estrategia (ej: "RSI + MACD")
2. Haz clic en "Escanear Indicadores"
3. Verifica que se muestran las señales

---

## 🐛 Solución de Problemas Comunes

### Problema 1: "ModuleNotFoundError: No module named 'flask_limiter'"

**Solución:**
```bash
# Reinstalar dependencias
pip install --upgrade Flask-Limiter Flask-CORS marshmallow python-json-logger prometheus-client
```

### Problema 2: "ImportError: cannot import name 'CORS'"

**Solución:**
```bash
# Reinstalar Flask-CORS
pip uninstall Flask-CORS
pip install Flask-CORS
```

### Problema 3: "Database is locked"

**Solución:**
```bash
# Eliminar el archivo de base de datos y recrear
del instance\scanner.db
python app.py  # Se creará automáticamente
```

### Problema 4: "Port 5000 is already in use"

**Solución:**
```bash
# Usar otro puerto
set PORT=5001
python app.py

# O matar el proceso que está usando el puerto
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Problema 5: Tests fallan con "ImportError"

**Solución:**
```bash
# Asegurarse de estar en el entorno virtual
venv\Scripts\activate

# Reinstalar dependencias de testing
pip install --upgrade pytest pytest-cov pytest-mock pytest-flask
```

---

## 📊 Variables de Entorno Disponibles

```bash
# Modo debug
set FLASK_DEBUG=1

# Host
set HOST=127.0.0.1

# Puerto
set PORT=5000

# Base de datos (para producción)
set DATABASE_URL=postgresql://user:pass@localhost:5432/scanner
```

---

## 🎓 Comandos Útiles

```bash
# Verificar versión de Python
python --version

# Verificar paquetes instalados
pip list | findstr -i "flask limiter cors marshmallow"

# Actualizar pip
python -m pip install --upgrade pip

# Limpiar caché de pip
pip cache purge

# Ver archivos del proyecto
dir /B

# Ver procesos de Python
tasklist | findstr python
```

---

## ✅ Checklist de Verificación

Antes de continuar con la Fase 2, verifica:

- [ ] Entorno virtual activado
- [ ] Todas las dependencias instaladas sin errores
- [ ] Script de verificación pasa sin errores
- [ ] Tests ejecutan correctamente (≥70% cobertura)
- [ ] Aplicación inicia sin errores
- [ ] Health check retorna "healthy"
- [ ] Métricas están disponibles en `/metrics`
- [ ] Dashboard carga correctamente en el navegador
- [ ] Puedes agregar un ticker desde `/admin`
- [ ] Puedes sincronizar datos desde el dashboard
- [ ] Puedes escanear señales desde el dashboard

---

## 📝 Notas Importantes

1. **Primera ejecución:** La primera vez que ejecutes la aplicación, se creará automáticamente la base de datos en `instance/scanner.db`.

2. **Tickers iniciales:** Si no hay tickers, puedes agregar los de ejemplo ejecutando:
   ```bash
   curl -X POST http://localhost:5000/api/seed
   ```

3. **Rate limiting:** Si excedes los límites (200/día, 50/hora), recibirás error 429. Espera unos minutos antes de volver a intentar.

4. **Logs:** Los logs ahora están en formato JSON para mejor análisis. Puedes verlos en la terminal donde ejecutas la aplicación.

5. **Métricas:** Las métricas de Prometheus están disponibles en `http://localhost:5000/metrics` para integración con sistemas de monitoreo.

---

## 🚀 Siguiente Fase

Una vez verificado que la Fase 1 funciona correctamente, puedes proceder con la **Fase 2** que incluye:

1. **Alembic Migrations** - Control de versiones del esquema
2. **Backups Automáticos** - Protección de datos
3. **Configuración por Ambiente** - Separación de dev/test/prod
4. **Docker Multi-Stage** - Imágenes más eficientes
5. **GitHub Actions CI/CD** - Pipeline automatizado

---

**¿Necesitas ayuda con algún problema?**
Revisa el archivo [`plans/fase1_implementada.md`](plans/fase1_implementada.md) para más detalles sobre la implementación.
