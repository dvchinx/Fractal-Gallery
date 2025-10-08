# Generador de Arte con IA - Fractales 🎨

Un generador de arte fractal optimizado que crea imágenes matemáticamente hermosas usando algoritmos eficientes y compilación JIT con Numba.

## 🚀 Características Principales

- **🌀 Fractales de Mandelbrot**: Con zoom profundo y exploración de puntos interesantes
- **🎭 Fractales de Julia**: 10+ presets famosos + constantes personalizadas
- **⚡ Ultra-optimizado**: Numba JIT compilation para velocidad extrema
- **🎨 Esquemas de colores**: 16+ colormaps organizados por categorías
- **📁 Gestión inteligente**: Auto-guardado con metadatos y miniaturas
- **🌐 Galería HTML**: Visualización web interactiva de tus creaciones
- **🎛️ Presets de calidad**: Desde preview hasta ultra 4K para impresión

## 📦 Instalación y Configuración

### Requisitos
- Python 3.8+
- 4GB RAM recomendado para imágenes de alta resolución

### Instalación
```bash
# Clonar/descargar el proyecto
cd fractal-gallery

# Instalar dependencias (se creará un virtual environment automáticamente)
pip install -r requirements.txt
```

### Verificar instalación
```bash
python main.py info
```

## 🎯 Guía de Uso

### Comandos Básicos

```bash
# Ver ayuda completa
python main.py --help

# Información del sistema
python main.py info

# Mandelbrot básico
python main.py mandelbrot

# Julia clásico
python main.py julia --julia-c classic

# Galería HTML de todas las imágenes
python main.py gallery
```

### Fractales de Mandelbrot

```bash
# Mandelbrot con preset de alta calidad
python main.py mandelbrot --preset high

# Explorar punto interesante con zoom
python main.py mandelbrot --explore seahorse_valley --zoom 50

# Personalizar completamente
python main.py mandelbrot --width 1920 --height 1080 --iterations 300 \
  --center-x -0.75 --center-y 0.1 --zoom 100 --colormap plasma
```

**Puntos de exploración disponibles:**
- `seahorse_valley`: Valle del caballito de mar
- `spiral`: Espirales matemáticas  
- `mini_mandelbrot`: Mini-Mandelbrot anidado
- `elephant_valley`: Valle del elefante

### Fractales de Julia

```bash
# Generar galería completa de Julia sets famosos
python main.py julia --gallery

# Julia sets con presets
python main.py julia --julia-c classic --preset ultra
python main.py julia --julia-c dragon --colormap inferno
python main.py julia --julia-c spiral --zoom 2

# Constante personalizada
python main.py julia --julia-c "0.285+0.01i" --iterations 200
```

**Presets de Julia disponibles:**
- `classic`: El Julia clásico (-0.7+0.27015i)
- `dragon`: Forma de dragón (-0.8+0.156i)
- `spiral`: Espirales (-0.7-0.3i)
- `lightning`: Rayos/relámpagos (-0.54+0.54i)
- `dendrite`: Estructura dendrítica (-0.235+0.85i)
- `rabbit`: Conejo de Douady (-0.123+0.745i)
- `airplane`: Forma de avión (-0.75+0.1i)
- `galaxy`: Estructura galáctica (0.285+0.01i)
- `flower`: Pétalos florales (-0.4+0.6i)
- `seahorse`: Caballito de mar (-0.75+0.11i)

## 🎛️ Configuración Avanzada

### Presets de Calidad

| Preset | Resolución | Iteraciones | DPI | Uso recomendado |
|--------|------------|-------------|-----|-----------------|
| `preview` | 400x300 | 50 | 72 | Vista previa rápida |
| `standard` | 800x600 | 100 | 100 | Uso general |
| `high` | 1920x1080 | 200 | 150 | Pantalla HD |
| `ultra` | 3840x2160 | 500 | 300 | 4K/8K |
| `print` | 3000x2000 | 300 | 300 | Impresión de calidad |

### Esquemas de Colores

```bash
# Colores cálidos
--colormap hot|plasma|inferno|magma

# Colores fríos  
--colormap viridis|cool|winter|blues

# Artísticos
--colormap rainbow|hsv|spring|summer

# Clásicos
--colormap gray|bone|copper|seismic
```

### Parámetros Completos

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--width`, `--height` | Resolución en píxeles | `--width 1920 --height 1080` |
| `--iterations` | Máx iteraciones (detalle) | `--iterations 300` |
| `--zoom` | Factor de zoom | `--zoom 100` |
| `--center-x`, `--center-y` | Centro del fractal | `--center-x -0.75 --center-y 0.1` |
| `--colormap` | Esquema de colores | `--colormap plasma` |
| `--preset` | Preset de calidad | `--preset ultra` |
| `--output` | Archivo de salida | `--output mi_fractal.png` |
| `--show`/`--no-show` | Mostrar resultado | `--no-show` |
| `--verbose`/`--quiet` | Información detallada | `--quiet` |

## 📂 Estructura del Proyecto

```
data-analysis/
├── main.py                    # Script principal
├── requirements.txt           # Dependencias Python
├── README.md                 # Esta documentación
├── src/                      # Código fuente
│   ├── mandelbrot.py         # Generador de Mandelbrot optimizado
│   ├── julia.py              # Generador de Julia con presets
│   ├── config_manager.py     # Sistema de configuración
│   └── file_utils.py         # Gestión de archivos y metadatos
├── config/                   # Archivos de configuración
│   └── fractal_config.yaml   # Configuración principal
├── output/                   # Imágenes generadas
│   ├── mandelbrot/           # Fractales de Mandelbrot
│   ├── julia/                # Fractales de Julia
│   ├── thumbnails/           # Miniaturas automáticas
│   ├── metadata/             # Metadatos YAML
│   └── gallery/              # Galerías HTML
└── docs/                     # Documentación adicional
```

## 🎨 Ejemplos Prácticos

### Crear una serie de exploraciones
```bash
# Serie de zoom en el valle del caballito de mar
python main.py mandelbrot --explore seahorse_valley --zoom 10 --output seahorse_01.png
python main.py mandelbrot --explore seahorse_valley --zoom 50 --output seahorse_02.png  
python main.py mandelbrot --explore seahorse_valley --zoom 200 --output seahorse_03.png
```

### Comparar esquemas de colores
```bash
# Mismo fractal con diferentes colores
python main.py julia --julia-c classic --colormap hot --output julia_hot.png
python main.py julia --julia-c classic --colormap plasma --output julia_plasma.png
python main.py julia --julia-c classic --colormap viridis --output julia_viridis.png
```

### Generar colección completa
```bash
# Galería completa de Julia sets
python main.py julia --gallery

# Mandelbrot en múltiples calidades
python main.py mandelbrot --preset standard --output mandelbrot_std.png
python main.py mandelbrot --preset high --output mandelbrot_hd.png
python main.py mandelbrot --preset ultra --output mandelbrot_4k.png
```

## 🔧 Personalización y Configuración

### Archivo de configuración (`config/fractal_config.yaml`)

El archivo de configuración permite personalizar:
- Resoluciones y calidades por defecto
- Puntos de exploración personalizados  
- Esquemas de colores nuevos
- Límites de memoria y rendimiento
- Organización de archivos de salida

### Estructura de metadatos

Cada imagen generada incluye un archivo YAML con:
- Parámetros completos de generación
- Información técnica del algoritmo
- Timestamp y estadísticas de rendimiento
- Hash único para evitar duplicados

## ⚡ Optimización y Rendimiento

### Numba JIT Compilation
- **Primera ejecución**: ~30-60 segundos (compilación)
- **Ejecuciones siguientes**: Ultra-rápidas (código nativo)
- **Paralelización**: Automática en CPUs multi-core
- **Memoria**: Optimizada para datasets grandes

### Consejos de rendimiento
```bash
# Para maximum velocidad en imágenes grandes
python main.py mandelbrot --preset ultra --iterations 200

# Para exploración rápida
python main.py mandelbrot --preset preview --show

# Para lotes grandes
python main.py julia --gallery --no-show
```

## 🚀 Extensibilidad

El proyecto está diseñado para ser extensible:

### Agregar nuevos tipos de fractales
1. Crear nuevo módulo en `src/`
2. Implementar funciones con decorador `@jit`
3. Agregar comandos en `main.py`

### Personalizar configuración
1. Editar `config/fractal_config.yaml`
2. Agregar nuevos presets o colormaps
3. Definir puntos de exploración personalizados

## 🎯 Próximas Características

- **Burning Ship fractals**: Variación del Mandelbrot
- **Newton fractals**: Fractales basados en el método de Newton
- **Animaciones**: Secuencias de zoom y transformación
- **Arte procedural**: Algoritmos generativos adicionales
- **Interfaz web**: Dashboard interactivo con Streamlit
- **Modo batch**: Procesamiento masivo automatizado

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Áreas de interés:
- Nuevos algoritmos de fractales
- Optimizaciones de rendimiento
- Esquemas de colores personalizados
- Documentación y ejemplos

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo licencia MIT.

---

**¡Disfruta creando arte matemático! 🎨✨**

Para soporte o preguntas, consulta los archivos de ejemplo en la carpeta `docs/` o revisa los metadatos generados automáticamente.