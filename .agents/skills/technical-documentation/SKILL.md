# Technical Documentation Skill

## Descripción
Esta habilidad proporciona conocimientos y capacidades para crear, mantener y mejorar la documentación técnica de un proyecto. Incluye desde la planificación inicial hasta la actualización continua de la documentación.

## Requisitos Previos
- Conocimientos básicos del proyecto a documentar
- Familiaridad con herramientas de documentación (Markdown, reStructuredText, etc.)
- Comprensión de la audiencia objetivo (desarrolladores, usuarios, etc.)

## Tipos de Documentación

### 1. Documentación de Usuario
- Guías de instalación y configuración
- Tutoriales paso a paso
- Referencia de API
- Preguntas frecuentes (FAQ)

### 2. Documentación de Desarrollador
- Guías de contribución
- Arquitectura del sistema
- Guías de desarrollo
- Referencia de código

### 3. Documentación de Operaciones
- Guías de despliegue
- Procedimientos de mantenimiento
- Plan de recuperación ante desastres
- Guías de monitoreo

## Herramientas de Documentación

### Markdown
```markdown
# Encabezado 1
## Encabezado 2

**Texto en negrita**
*Texto en cursiva*

[Enlace](https://ejemplo.com)

![Imagen](ruta/a/imagen.png)

```python
def funcion():
    return "Hola"
```

- Lista desordenada
1. Lista ordenada
```

### reStructuredText
```rst
Encabezado 1
===========

Encabezado 2
-----------

**Texto en negrita**
*Texto en cursiva*

`Enlace`_

.. _Enlace: https://ejemplo.com

.. image:: ruta/a/imagen.png

.. code-block:: python

   def funcion():
       return "Hola"

- Lista desordenada
#. Lista ordenada
```

### Herramientas de Generación de Documentación
- **Sphinx**: Para proyectos Python
- **MkDocs**: Para sitios estáticos con Markdown
- **Docusaurus**: Para documentación de React/JavaScript
- **Hugo**: Para sitios estáticos rápidos
- **GitBook**: Para documentación colaborativa

## Estructura de Documentación

### Estructura Típica
```
docs/
├── README.md              # Introducción
├── getting-started/       # Guías de inicio
│   ├── installation.md
│   └── quick-start.md
├── user-guide/            # Guías de usuario
│   ├── features.md
│   └── tutorials.md
├── developer-guide/       # Guías de desarrollador
│   ├── architecture.md
│   ├── contributing.md
│   └── api-reference.md
├── operations/             # Documentación de operaciones
│   ├── deployment.md
│   └── monitoring.md
└── assets/                # Imágenes y recursos
    └── images/
```

## Mejores Prácticas

### 1. Escribir para la Audiencia Correcta
- Identifica quién leerá la documentación
- Ajusta el nivel de detalle según la audiencia
- Usa ejemplos relevantes y claros

### 2. Mantener la Documentación Actualizada
- Actualiza la documentación cuando cambie el código
- Usa etiquetas de versión para documentación histórica
- Revisa y actualiza regularmente

### 3. Usar un Lenguaje Claro y Conciso
- Evita jerga innecesaria
- Usa oraciones cortas y directas
- Incluye ejemplos prácticos

### 4. Incluir Diagramas y Visualizaciones
- Usa diagramas de arquitectura para sistemas complejos
- Incluye capturas de pantalla para interfaces de usuario
- Usa diagramas de flujo para procesos

### 5. Documentar el "Por Qué", No Solo el "Qué"
- Explica las decisiones de diseño
- Incluye el contexto histórico
- Documenta las limitaciones y trade-offs

## Automatización de Documentación

### Documentación Automática de Código
```python
# Ejemplo con Sphinx

def calcular_promedio(numeros):
    """
    Calcula el promedio de una lista de números.

    Args:
        numeros (list): Lista de números.

    Returns:
        float: Promedio de los números.

    Raises:
        ValueError: Si la lista está vacía.

    Example:
        >>> calcular_promedio([1, 2, 3, 4, 5])
        3.0
    """
    if not numeros:
        raise ValueError("La lista no puede estar vacía")
    return sum(numeros) / len(numeros)
```

### Generación de Documentación con Sphinx
```bash
# Instalar Sphinx
pip install sphinx sphinx-rtd-theme

# Crear directorio de documentación
mkdir docs
cd docs

# Inicializar Sphinx
sphinx-quickstart

# Generar documentación desde código
sphinx-apidoc -o . ../src

# Construir documentación
make html
```

### Integración con CI/CD
```yaml
# Ejemplo con GitHub Actions
name: Build Documentation

on:
  push:
    branches: [main]

jobs:
  build-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: |
          pip install sphinx sphinx-rtd-theme
      - name: Build documentation
        run: |
          cd docs
          make html
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/_build/html
```

## Revisión de Documentación

### Checklist de Revisión
- [ ] La documentación es clara y fácil de entender
- [ ] Los ejemplos son correctos y funcionan
- [ ] La documentación está actualizada con el código
- [ ] No hay errores ortográficos o gramaticales
- [ ] Los enlaces funcionan correctamente
- [ ] Las imágenes se muestran correctamente
- [ ] La estructura es lógica y fácil de navegar

## Recursos Adicionales
- [Write the Docs](https://www.writethedocs.org/)
- [Diátaxis Framework](https://diataxis.fr/)
- [Google Technical Writing](https://developers.google.com/tech-writing)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [MkDocs Documentation](https://www.mkdocs.org/)
