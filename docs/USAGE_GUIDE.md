# 📚 Guía Completa de Uso - Fractal Gallery

## 📋 Tabla de Contenidos

- [🎯 Comandos Esenciales](#-comandos-esenciales)
- [🌀 Fractales de Mandelbrot](#-fractales-de-mandelbrot)
- [🎭 Fractales de Julia](#-fractales-de-julia)
- [📊 Presets y Parámetros](#-presets-y-parámetros)
- [🎨 Esquemas de Colores](#-esquemas-de-colores)
- [🎨 Ejemplos Prácticos](#-ejemplos-prácticos)
- [⚙️ Configuración Avanzada](#️-configuración-avanzada)
- [🔧 Personalización](#-personalización)

## 🎯 Comandos Esenciales

### ⚡ Inicio Rápido

```bash
# 🔍 Ver ayuda completa
python main.py --help

# ℹ️ Información del sistema  
python main.py info

# 🌀 Tu primer Mandelbrot
python main.py mandelbrot

# 🎭 Tu primer Julia
python main.py julia --julia-c classic

# 🖼️ Generar galería HTML
python main.py gallery
```

## 🌀 Fractales de Mandelbrot

### Comandos Básicos

```bash
# Mandelbrot con preset de alta calidad
python main.py mandelbrot --preset high

# Explorar punto interesante con zoom
python main.py mandelbrot --explore seahorse_valley --zoom 50

# Personalizar completamente
python main.py mandelbrot --width 1920 --height 1080 --iterations 300 \
  --center-x -0.75 --center-y 0.1 --zoom 100 --colormap plasma
```

### 🎯 Puntos de Exploración Disponibles

| Punto | Coordenadas | Descripción |
|-------|-------------|-------------|
| `seahorse_valley` | -0.75+0.1i | Valle del caballito de mar |
| `spiral` | -0.1+0.651i | Espirales matemáticas |
| `mini_mandelbrot` | -0.2+1.1i | Mini-Mandelbrot anidado |
| `elephant_valley` | 0.25+0.0i | Valle del elefante |

### Ejemplos de Exploración

```bash
# Serie de zoom en el valle del caballito de mar
python main.py mandelbrot --explore seahorse_valley --zoom 10 --output seahorse_01.png
python main.py mandelbrot --explore seahorse_valley --zoom 50 --output seahorse_02.png  
python main.py mandelbrot --explore seahorse_valley --zoom 200 --output seahorse_03.png

# Exploración manual con coordenadas
python main.py mandelbrot --center-x -0.7463 --center-y 0.1102 --zoom 1000 \
  --iterations 500 --colormap inferno --preset ultra
```

## 🎭 Fractales de Julia

### Comandos Básicos

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

### 🎭 Presets de Julia Disponibles

| Preset | Constante | Descripción | Características |
|--------|-----------|-------------|-----------------|
| `classic` | -0.7+0.27015i | El Julia clásico | Forma simétrica elegante |
| `dragon` | -0.8+0.156i | Forma de dragón | Estructuras fractales complejas |
| `spiral` | -0.7-0.3i | Espirales | Patrones en espiral |
| `lightning` | -0.54+0.54i | Rayos/relámpagos | Ramificaciones eléctricas |
| `dendrite` | -0.235+0.85i | Estructura dendrítica | Patrones como árboles |
| `rabbit` | -0.123+0.745i | Conejo de Douady | Forma icónica |
| `airplane` | -0.75+0.1i | Forma de avión | Silueta aeronáutica |
| `galaxy` | 0.285+0.01i | Estructura galáctica | Patrones espirales |
| `flower` | -0.4+0.6i | Pétalos florales | Simetría radial |
| `seahorse` | -0.75+0.11i | Caballito de mar | Formas orgánicas |

### Exploración de Constantes Personalizadas

```bash
# Explorar variaciones de una constante base
python main.py julia --julia-c "-0.7+0.27i" --output julia_base.png
python main.py julia --julia-c "-0.7+0.28i" --output julia_var1.png
python main.py julia --julia-c "-0.7+0.26i" --output julia_var2.png

# Constantes con diferentes partes imaginarias
python main.py julia --julia-c "0.3+0.5i" --colormap plasma
python main.py julia --julia-c "0.3-0.5i" --colormap viridis
```

## 📊 Presets y Parámetros

### 🎛️ Presets de Calidad

| Preset | Resolución | Iteraciones | DPI | Tiempo* | Uso recomendado |
|--------|------------|-------------|-----|---------|-----------------|
| `preview` | 400×300 | 50 | 72 | ~2s | Vista previa rápida |
| `standard` | 800×600 | 100 | 100 | ~5s | Uso general |
| `high` | 1920×1080 | 200 | 150 | ~15s | Pantalla HD |
| `ultra` | 3840×2160 | 500 | 300 | ~60s | 4K/8K |
| `print` | 3000×2000 | 300 | 300 | ~45s | Impresión de calidad |

*Tiempos aproximados en CPU moderna después de compilación JIT

### ⚙️ Parámetros Completos

| Parámetro | Tipo | Rango | Descripción | Ejemplo |
|-----------|------|-------|-------------|---------|
| `--width`, `--height` | int | 100-8000 | Resolución en píxeles | `--width 1920 --height 1080` |
| `--iterations` | int | 10-2000 | Máx iteraciones (detalle) | `--iterations 300` |
| `--zoom` | float | 0.1-10000 | Factor de zoom | `--zoom 100.5` |
| `--center-x`, `--center-y` | float | -2.0 a 2.0 | Centro del fractal | `--center-x -0.75 --center-y 0.1` |
| `--colormap` | str | Ver tabla | Esquema de colores | `--colormap plasma` |
| `--preset` | str | Ver tabla | Preset de calidad | `--preset ultra` |
| `--output` | path | - | Archivo de salida | `--output mi_fractal.png` |
| `--show`/`--no-show` | bool | - | Mostrar resultado | `--no-show` |
| `--verbose`/`--quiet` | bool | - | Información detallada | `--quiet` |

## 🎨 Esquemas de Colores

### 🔥 Colores Cálidos

```bash
--colormap hot      # Rojo-amarillo clásico - ideal para fractales dramáticos
--colormap plasma   # Violeta-amarillo moderno - científico y elegante
--colormap inferno  # Negro-rojo-amarillo - contraste máximo
--colormap magma    # Negro-violeta-blanco - suave y profesional
```

### ❄️ Colores Fríos

```bash
--colormap viridis  # Verde-azul científico - estándar científico
--colormap cool     # Cian-magenta - contraste frío
--colormap winter   # Azul-verde - natural y orgánico
--colormap blues    # Gradiente de azules - minimalista
```

### 🌈 Colores Artísticos

```bash
--colormap rainbow  # Espectro completo - vibrante y llamativo
--colormap hsv      # Matiz-saturación - artístico
--colormap spring   # Magenta-amarillo - primaveral
--colormap summer   # Verde-amarillo - cálido y natural
```

### ⚫ Colores Clásicos

```bash
--colormap gray     # Escala de grises - elegante y atemporal
--colormap bone     # Hueso - suave y orgánico
--colormap copper   # Cobre - cálido metálico
--colormap seismic  # Sismográfico - científico
```

## 🎨 Ejemplos Prácticos

### 🔄 Crear una Serie de Exploraciones

```bash
# Serie de zoom progresivo
for zoom in 1 10 50 200 1000; do
  python main.py mandelbrot --explore seahorse_valley --zoom $zoom \
    --output "seahorse_zoom_${zoom}.png" --preset high
done

# Serie con diferentes centros
python main.py mandelbrot --center-x -0.75 --center-y 0.1 --zoom 100 --output center1.png
python main.py mandelbrot --center-x -0.235 --center-y 0.85 --zoom 100 --output center2.png
python main.py mandelbrot --center-x 0.285 --center-y 0.01 --zoom 100 --output center3.png
```

### 🎨 Comparar Esquemas de Colores

```bash
# Mismo fractal con diferentes colores
julia_constant="classic"
for colormap in hot plasma viridis rainbow gray; do
  python main.py julia --julia-c $julia_constant --colormap $colormap \
    --output "julia_${colormap}.png" --preset high
done
```

### 📦 Generar Colección Completa

```bash
# Galería completa de Julia sets
python main.py julia --gallery --preset high --no-show

# Mandelbrot en múltiples calidades
for preset in preview standard high ultra; do
  python main.py mandelbrot --preset $preset \
    --output "mandelbrot_${preset}.png" --no-show
done

# Exploración automática de puntos interesantes
for point in seahorse_valley spiral mini_mandelbrot elephant_valley; do
  python main.py mandelbrot --explore $point --zoom 50 \
    --output "exploration_${point}.png" --preset high --no-show
done
```

### 🔬 Investigación Matemática

```bash
# Análisis de convergencia con diferentes iteraciones
for iterations in 50 100 200 500 1000; do
  python main.py mandelbrot --iterations $iterations \
    --output "convergence_${iterations}.png" --preset standard --no-show
done

# Exploración de la frontera del conjunto
python main.py mandelbrot --center-x -0.7463 --center-y 0.1102 \
  --zoom 10000 --iterations 1000 --colormap inferno --preset ultra

# Julia sets con variaciones mínimas
base_real=-0.7
for i in {0..10}; do
  imag=$(echo "0.27 + $i * 0.001" | bc -l)
  python main.py julia --julia-c "${base_real}+${imag}i" \
    --output "julia_variation_${i}.png" --preset high --no-show
done
```

## ⚙️ Configuración Avanzada

### 📄 Archivo de Configuración

Editar `config/fractal_config.yaml`:

```yaml
# Configuración personalizada
defaults:
  width: 1920
  height: 1080
  iterations: 200
  colormap: plasma

# Puntos de exploración personalizados
exploration_points:
  my_point:
    x: -0.123456
    y: 0.654321
    description: "Mi punto especial"

# Presets personalizados
custom_presets:
  my_preset:
    width: 2560
    height: 1440
    iterations: 300
    dpi: 200
```

### 🎯 Optimización de Rendimiento

```bash
# Para máxima velocidad en imágenes grandes
python main.py mandelbrot --preset ultra --iterations 200 --no-show

# Para exploración rápida interactiva  
python main.py mandelbrot --preset preview --show

# Para procesamiento en lotes
python main.py julia --gallery --no-show --quiet

# Compilación JIT en segundo plano
python main.py mandelbrot --preset preview --no-show  # Primera ejecución
# Las siguientes serán ultra-rápidas
```

### 📊 Monitoreo de Rendimiento

```bash
# Con información detallada de tiempo
python main.py mandelbrot --preset high --verbose

# Modo silencioso para scripts
python main.py julia --gallery --quiet --no-show

# Información del sistema
python main.py info
```

## 🔧 Personalización

### 🎨 Crear Nuevos Esquemas de Colores

Para agregar colormaps personalizados, edita el archivo de configuración:

```yaml
custom_colormaps:
  sunset:
    colors: ["#000000", "#FF4500", "#FFD700", "#FFFFFF"]
  ocean:
    colors: ["#000080", "#0000FF", "#00FFFF", "#FFFFFF"]
```

### 🌀 Definir Puntos de Exploración

```yaml
exploration_points:
  spiral_arm:
    x: -0.1
    y: 0.651
    zoom: 100
    description: "Brazo espiral principal"
  detail_zoom:
    x: -0.7463
    y: 0.1102
    zoom: 1000
    description: "Detalle con alto zoom"
```

### ⚡ Scripts de Automatización

Crear `generate_gallery.sh`:

```bash
#!/bin/bash
# Script para generar galería completa

echo "Generando fractales de Mandelbrot..."
for point in seahorse_valley spiral mini_mandelbrot; do
  python main.py mandelbrot --explore $point --preset high --no-show
done

echo "Generando fractales de Julia..."
python main.py julia --gallery --preset high --no-show

echo "Creando galería HTML..."
python main.py gallery

echo "¡Galería completa generada!"
```

## 🔍 Casos de Uso Avanzados

### 🎬 Secuencias de Animación

```bash
# Crear frames para animación de zoom
for i in {1..30}; do
  zoom=$(echo "scale=2; 2^($i/3)" | bc)
  python main.py mandelbrot --explore seahorse_valley --zoom $zoom \
    --output "animation/frame_$(printf "%03d" $i).png" --preset standard --no-show
done
```

### 🔬 Análisis Científico

```bash
# Mapeo de convergencia detallado
python main.py mandelbrot --iterations 2000 --preset ultra \
  --center-x -0.7463 --center-y 0.1102 --zoom 10000

# Comparación de diferentes algoritmos (futuro)
python main.py mandelbrot --algorithm escape_time --preset high
python main.py mandelbrot --algorithm continuous --preset high
```

### 🎨 Arte Generativo

```bash
# Serie artística con paletas coordinadas
palettes=("inferno" "plasma" "viridis" "magma")
julia_sets=("classic" "dragon" "spiral" "lightning")

for i in {0..3}; do
  python main.py julia --julia-c ${julia_sets[$i]} \
    --colormap ${palettes[$i]} --preset ultra \
    --output "art_series_$(($i+1)).png" --no-show
done
```

---

## 💡 Tips y Trucos

### ⚡ Rendimiento
- Primera ejecución siempre es lenta (compilación JIT)
- Usa `--no-show` para procesamiento en lotes
- `--quiet` reduce overhead de salida
- Preset `preview` para exploración rápida

### 🎨 Calidad Visual
- `--preset ultra` para impresiones
- Aumenta `--iterations` para más detalle
- Experimenta con diferentes `--colormap`
- Usa zoom alto para detalles fractales

### 📁 Organización
- Los archivos se guardan automáticamente con timestamps
- Metadatos en YAML para cada imagen
- Miniaturas generadas automáticamente
- Galería HTML para visualización web

### 🔧 Debugging
- `--verbose` para información detallada
- `python main.py info` para verificar sistema
- Revisa los archivos de metadatos para parámetros exactos