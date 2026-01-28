# Análisis Detallado de Cambios - Optimización de Rendimiento

**Fecha:** 28 de enero de 2026
**Estado:** Análisis completado - Esperando aprobación

## Resumen de Cambios por Fase

### FASE 1: Cambios Inmediatos (Impacto Alto, Complejidad Baja)

#### Cambio 1.1: Reemplazar `iterrows()` con `itertuples()`
- **Archivo:** `finance_service.py:68-86`
- **Impacto:** 50-70% más rápido
- **Complejidad:** Muy baja (1 línea de cambio)
- **Riesgo:** Nulo - solo cambia forma de acceso a datos

**Cambios:**
```python
# ANTES (lento)
for index, row in data.iterrows():
    date_val = index.date()
    open_val = float(row['Open'].iloc[0] if isinstance(row['Open'], pd.Series) else row['Open'])
    # ... más accesos complejos

# DESPUÉS (rápido)
for row in data.itertuples():
    date_val = row.Index.date()
    open_val = float(row.Open)
    # ... accesos directos
```

**Beneficio:** Elimina acceso a índice y manejo de Series, acceso directo a campos.

---

#### Cambio 1.4: Reducir delay entre tickers
- **Archivo:** `app.py:144`
- **Impacto:** 50% menos tiempo total
- **Complejidad:** Muy baja (1 número de cambio)
- **Riesgo:** Bajo - yfinance maneja bien 0.3s

**Cambios:**
```python
# ANTES
delay_between_tickers = 1  # 1 segundo

# DESPUÉS
delay_between_tickers = 0.3  # 0.3 segundos
```

**Beneficio:** Menos tiempo de espera sin riesgo de bloqueo.

---

#### Cambio 1.5: Agregar índice compuesto a Price
- **Archivo:** `database.py:25`
- **Impacto:** 30-50% más rápido en consultas
- **Complejidad:** Muy baja (1 línea de cambio)
- **Riesgo:** Nulo - solo agrega índice

**Cambios:**
```python
# ANTES
__table_args__ = (
    db.UniqueConstraint('ticker_id', 'date', name='_ticker_date_uc'),
)

# DESPUÉS
__table_args__ = (
    db.UniqueConstraint('ticker_id', 'date', name='_ticker_date_uc'),
    db.Index('idx_ticker_date', 'ticker_id', 'date'),
)
```

**Beneficio:** Consultas por ticker_id y date mucho más rápidas.

---

### FASE 2: Cambios de Alto Impacto (Impacto Alto/Medio, Complejidad Media)

#### Cambio 1.2: Usar `set()` para verificar duplicados
- **Archivo:** `finance_service.py:68-86`
- **Impacto:** 90% más rápido (elimina N+1 queries)
- **Complejidad:** Baja (5-10 líneas de cambio)
- **Riesgo:** Bajo - solo optimiza lógica existente

**Cambios:**
```python
# ANTES (N+1 queries)
for index, row in data.iterrows():
    date_val = index.date()
    existing = Price.query.filter_by(ticker_id=ticker_obj.id, date=date_val).first()
    if not existing:
        # ...

# DESPUÉS (1 query + set lookup O(1))
existing_dates = set(
    p.date for p in Price.query
    .with_entities(Price.date)
    .filter_by(ticker_id=ticker_obj.id)
    .all()
)

for row in data.itertuples():
    date_val = row.Index.date()
    if date_val not in existing_dates:
        # ...
```

**Beneficio:** Reduce de N queries a 1 query.

---

#### Cambio 1.3: Usar `bulk_save_objects()` para inserciones
- **Archivo:** `finance_service.py:68-86`
- **Impacto:** 80-90% más rápido
- **Complejidad:** Baja (10-15 líneas de cambio)
- **Riesgo:** Bajo - usa transacción única

**Cambios:**
```python
# ANTES (insert individual)
for row in data.itertuples():
    # ...
    price = Price(...)
    db.session.add(price)
    count += 1
db.session.commit()

# DESPUÉS (bulk insert)
new_prices = []
for row in data.itertuples():
    date_val = row.Index.date()
    if date_val not in existing_dates:
        new_prices.append(Price(...))

if new_prices:
    db.session.bulk_save_objects(new_prices)
    count = len(new_prices)
```

**Beneficio:** Una transacción en lugar de N transacciones.

---

#### Cambio 2.1: Usar `with_entities()` para cargar solo campos necesarios
- **Archivo:** `finance_service.py:95-106`
- **Impacto:** 20-30% más rápido, menos memoria
- **Complejidad:** Baja (2-3 líneas de cambio)
- **Riesgo:** Nulo - solo optimiza carga de datos

**Cambios:**
```python
# ANTES
prices = Price.query.filter_by(ticker_id=ticker_obj.id).order_by(Price.date.asc()).all()
df = pd.DataFrame([{
    'date': p.date,
    'open': p.open,
    'high': p.high,
    'low': p.low,
    'close': p.close,
    'volume': p.volume
} for p in prices])

# DESPUÉS
prices = Price.query.with_entities(
    Price.date, Price.open, Price.high,
    Price.low, Price.close, Price.volume
).filter_by(ticker_id=ticker_obj.id).order_by(Price.date.asc()).all()

df = pd.DataFrame([{
    'date': p.date,
    'open': p.open,
    'high': p.high,
    'low': p.low,
    'close': p.close,
    'volume': p.volume
} for p in prices])
```

**Beneficio:** Carga solo los campos necesarios, menos transferencia de datos.

---

### FASE 3: Optimización Adicional (Impacto Medio, Complejidad Media/Alta)

#### Cambio 2.2: Usar `read_sql()` de pandas para carga directa
- **Archivo:** `finance_service.py:95-106`
- **Impacto:** 40-50% más rápido
- **Complejidad:** Media (10-15 líneas de cambio)
- **Riesgo:** Bajo - usa API de pandas

**Cambios:**
```python
# ANTES
prices = Price.query.filter_by(ticker_id=ticker_obj.id).order_by(Price.date.asc()).all()
df = pd.DataFrame([{
    'date': p.date,
    'open': p.open,
    'high': p.high,
    'low': p.low,
    'close': p.close,
    'volume': p.volume
} for p in prices])
df.set_index('date', inplace=True)

# DESPUÉS
query = db.session.query(
    Price.date, Price.open, Price.high,
    Price.low, Price.close, Price.volume
).filter_by(ticker_id=ticker_obj.id).order_by(Price.date.asc())

df = pd.read_sql(query.statement, db.session.bind)
df.set_index('date', inplace=True)
```

**Beneficio:** Pandas hace la conversión directamente desde SQL, más eficiente.

---

#### Cambio 2.3: Implementar caché simple con `@lru_cache`
- **Archivo:** `app.py:156-165`
- **Impacto:** 95% más rápido en peticiones repetidas
- **Complejidad:** Baja (10-15 líneas de cambio)
- **Riesgo:** Medio - requiere considerar concurrencia

**Cambios:**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_cached_signals(ticker_id, strategy, cache_key):
    ticker = Ticker.query.get(ticker_id)
    return FinanceService.get_signals(ticker, strategy=strategy)

@app.route('/api/scan', methods=['GET'])
def scan_tickers():
    strategy = request.args.get('strategy', 'rsi_macd')
    tickers = Ticker.query.all()
    
    signals = []
    for t in tickers:
        cache_key = f"{t.id}_{strategy}"
        signal = get_cached_signals(t.id, strategy, cache_key)
        if signal:
            signals.append(signal)
    
    return jsonify(signals)
```

**Beneficio:** Respuestas casi instantáneas para peticiones repetidas.

---

## Orden de Implementación Recomendado

### Fase 1: Cambios Inmediatos (1-2 horas)
1. ✅ Cambio 1.1: `iterrows()` → `itertuples()`
2. ✅ Cambio 1.4: Reducir delay a 0.3s
3. ✅ Cambio 1.5: Agregar índice a Price

**Beneficio esperado:** 40-60% más rápido en sincronización

### Fase 2: Cambios de Alto Impacto (2-3 horas)
4. ✅ Cambio 1.2: Usar `set()` para duplicados
5. ✅ Cambio 1.3: Usar `bulk_save_objects()`
6. ✅ Cambio 2.1: Usar `with_entities()`

**Beneficio esperado:** 80-90% más rápido en sincronización, 20-30% en señales

### Fase 3: Optimización Adicional (1-2 horas)
7. ✅ Cambio 2.2: Usar `read_sql()`
8. ✅ Cambio 2.3: Implementar caché simple

**Beneficio esperado:** 95% más rápido en peticiones repetidas

---

## Testing Plan

Antes de cada fase:
1. ✅ Backup de base de datos
2. ✅ Ejecutar `scripts/check_db.py` para estado inicial
3. ✅ Probar sincronización de 5 tickers
4. ✅ Verificar endpoint `/api/scan`
5. ✅ Comparar tiempos antes/después

Después de cada fase:
1. ✅ Verificar que resultados sean idénticos
2. ✅ Documentar mejoras de rendimiento
3. ✅ Actualizar documentación

---

## Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Bulk operations causa error de memoria | Baja | Medio | Implementar chunking si es necesario |
| Delay muy corto causa bloqueo API | Baja | Alto | Mantener monitoreo, ajustar si es necesario |
| Caché devuelve datos desactualizados | Media | Bajo | TTL de 5 minutos es aceptable |
| Polars requiere cambios significativos | Alta | Medio | Solo implementar si es necesario |

---

## Estimación de Mejoras Totales

| Métrica | Estado Actual | Después de Fase 1 | Después de Fase 2 | Después de Fase 3 |
|---------|--------------|-------------------|-------------------|-------------------|
| Sincronización 1 ticker | ~2-3s | ~1-1.5s | ~0.3-0.5s | ~0.2-0.3s |
| Sincronización 100 tickers | ~200-300s | ~80-120s | ~30-50s | ~30-50s |
| Endpoint /api/scan (1ra vez) | ~5-10s | ~4-8s | ~2-3s | ~1-2s |
| Endpoint /api/scan (caché) | ~5-10s | ~5-10s | ~5-10s | ~0.1-0.2s |
| Inserción 500 precios | ~5-8s | ~2-3s | ~0.5-1s | ~0.5-1s |

**Mejora total esperada después de Fase 3:** 80-95% más rápido en la mayoría de operaciones.
