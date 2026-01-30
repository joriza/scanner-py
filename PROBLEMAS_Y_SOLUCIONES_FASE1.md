# Problemas Identificados y Soluciones - Fase 1

**Fecha:** 29 de enero de 2026

## Resumen de Problemas

### 🔴 Problema 1: Error en app.py - Línea 88

**Error:** `TypeError: unsupported operand type(s) for -: 'datetime.datetime' and 'float'`

**Ubicación:** [`metrics.py`](metrics.py):88)
```python
elapsed = (datetime.now() - g.start_time).total_seconds()
```

**Causa:** `g.start_time` puede ser `None` o un número (segundos) en lugar de un objeto `datetime`.

**Solución:**
```python
# En metrics.py, línea 88
if g.start_time:
    elapsed = (datetime.now() - g.start_time).total_seconds()
else:
    elapsed = 0.0
```

---

### 🔴 Problema 2: Working Outside Application Context

**Error:** "Working outside of application context. This typically means that you attempted to use functionality that needed the current application. To solve this, set up an application context with app.app_context(). See the documentation for more information."

**Causa:** El script `scripts/run_with_debug.py` está ejecutando [`app.py`](app.py) con `exec()` directamente sin usar el contexto de Flask.

**Solución:** Ejecutar la aplicación normalmente:
```bash
python app.py
```

---

### 🟡 Problema 3: /favicon.ico No Encontrado (Error 404)

**Error:** "The requested URL was not found on server."

**Causa:** El navegador busca automáticamente `/favicon.ico` que no existe en el proyecto.

**Solución:** Agregar un archivo favicon.ico o ignorar este error (es solo informativo).

---

## Pasos para Corregir

### Paso 1: Corregir metrics.py

```python
# En metrics.py, línea 88
if hasattr(g, 'start_time') and g.start_time:
    elapsed = (datetime.now() - g.start_time).total_seconds()
else:
    elapsed = 0.0
```

### Paso 2: Ejecutar la aplicación correctamente

```bash
# No usar el script run_with_debug.py
python app.py
```

### Paso 3: Verificar que todo funciona

1. Abrir http://localhost:5000/health
2. Abrir http://localhost:5000/metrics
3. Abrir http://localhost:5000/admin
4. Abrir http://localhost:5000/

---

## Verificación de Dependencias

Si aún hay problemas con las importaciones, reinstala las dependencias:

```bash
# Desinstalar y reinstalar
pip uninstall flask-limiter flask-cors marshmallow python-json-logger prometheus-client
pip install flask-limiter flask-cors marshmallow python-json-logger prometheus-client
```

---

## Notas Importantes

1. **No ejecutes scripts directamente** - La aplicación debe ejecutarse con `python app.py`
2. **Contexto de Flask** - Los middlewares y configuración requieren que la aplicación se ejecute dentro del contexto de Flask
3. **Dependencias nuevas** - Asegúrate de instalar todas las dependencias de [`requirements.txt`](requirements.txt)

---

## Si los problemas persisten

Si después de seguir estos pasos los problemas continúan, por favor:

1. Copia y pega el traceback exacto del error
2. Ejecuta `python scripts/diagnostico_simple.py` para más detalles
3. Revisa los archivos modificados: [`app.py`](app.py), [`metrics.py`](metrics.py), [`schemas.py`](schemas.py)
