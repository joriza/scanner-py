# Documentación Técnica Detallada - Scanner Pro

## 1. Arquitectura del Sistema
El sistema es un scanner de activos financieros que opera sobre precios de cierre diarios, utilizando una base de datos local SQLite para persistencia y `yfinance` para la sincronización de datos.

## 2. Definición de Estrategias e Indicadores

### 🟢 Estrategia 1: RSI + MACD (1-RSI+MACD)
Orientada a detectar rebotes alcistas tras periodos de capitulación.
- **RSI (14)**:
    - **Sobreventa**: Detecta la fecha más reciente donde el RSI bajó de 30 en los últimos 365 días.
    - **Tendencia (Rebote)**: Identifica el primer cruce alcista del RSI sobre su Media Móvil Simple (SMA 14) ocurrido *posteriormente* a la última fecha de sobreventa detectada.
- **MACD (12, 26, 9)**:
    - **Zona de Oportunidad**: Cruce alcista (`MACD > Signal`) ocurrido estrictamente por debajo o igual a la línea de cero (`MACD <= 0`).
    - **Lógica de Estado (Inactivo/Rojo)**: La señal se apaga (rojo) si el cruce se vuelve bajista O si el MACD cruza por encima de cero, indicando que el activo ya no está en zona de compra ideal.

### 🔵 Estrategia 2: 3 EMAS (4, 9, 18) (Diaria + Semanal)
Estrategia de seguimiento de tendencia de alta sensibilidad (Multi-Timeframe).
- **Indicadores**: Medias Móviles Exponenciales (EMA) de 4, 9 y 18 períodos.
- **Condición Alcista**: `Precio Cierre > EMA 4 AND Precio Cierre > EMA 9 AND Precio Cierre > EMA 18`.
- **Temporalidad Diaria**: Basada en datos del día.
- **Temporalidad Semanal**: Generada mediante resampling de datos diarios hacia cierres de viernes (`W-FRI`). Captura la tendencia estructural.

## 3. Lógica de Ordenamiento (Jerarquía Estricta)
Para asegurar que las oportunidades más frescas aparezcan primero, el Dashboard aplica el siguiente algoritmo de clasificación en la Estrategia 2:

1.  **Criterio 1 (Actividad)**: Se asigna una puntuación. Los activos que cumplen la condición en **Ambas** temporalidades (Diario + Semanal) tienen prioridad máxima.
2.  **Criterio 2 (Semanal)**: Ante empate de puntuación, se ordena por la fecha **Semanal más reciente** (menor cantidad de días desde el cruce).
3.  **Criterio 3 (Diario - Desempate)**: Si la fecha semanal es idéntica (común en cierres de viernes), se ordena por la fecha **Diaria más reciente**.
4.  **Criterio 4 (Histórico)**: Finalmente, los activos que no cumplen hoy se muestran según cuándo fue la última vez que estuvieron activos.

## 4. Notas para Desarrolladores / Agentes AI
- **Frecuencia de Datos**: El sistema asume que la sincronización se realiza post-cierre de mercado.
- **Resampling Semanal**: Es crítico usar `W-FRI` para evitar proyecciones de fechas futuras (anomalía de días negativos corregida).
- **Interfaz**: El rendered es dinámico. El cambio de estrategia en el selector dispara una reconstrucción completa de los encabezados de la tabla y una reclasificación de los datos en tiempo real.
