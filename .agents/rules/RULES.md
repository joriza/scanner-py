# Reglas para Agentes de IA

## Descripción
Este archivo define las reglas y directrices que deben seguir los agentes de IA al trabajar en este repositorio.

## Reglas Generales

### Idioma
- Todas las comunicaciones, documentación y mensajes de commit deben estar en español.

### Formato de Commits
- Asunto en presente indicativo, máximo 72 caracteres
- Cuerpo opcional separado por línea en blanco
- Ejemplo: `Corregir validación en POST /api/tickers`

### Git Workflow
- Crear rama para cada tarea/feature
- Publicar rama inmediatamente: `git push -u origin nombre-rama`
- Realizar push después de cada commit relevante
- Pull requests en español con descripción de cambios

### Calidad de Código
- Seguir convenciones del lenguaje (PEP 8 para Python)
- Agregar tests para nuevas funcionalidades
- Documentar código complejo
- Ejecutar linters/formatters antes de commits

### Seguridad
- No incluir credenciales en el código
- Usar variables de entorno para configuración sensible
- Validar todas las entradas de usuario

## Reglas Específicas del Proyecto

### Base de Datos
- Usar SQLite (database.py)
- Sincronización incremental vía FinanceService.sync_ticker_data

### API
- Todas las señales técnicas calculadas en memoria
- Usar FinanceService.get_signals(ticker, strategy)

### Lógica de Negocio
- Resampling Daily -> Weekly usando 'W-FRI'
- MACD estándar (12, 26, 9)
- RSI periodo 14

## Excepciones
- Si una rama es experimental y no debe publicarse, documentarlo explícitamente
- Solicitar aprobación para desviaciones de las reglas
