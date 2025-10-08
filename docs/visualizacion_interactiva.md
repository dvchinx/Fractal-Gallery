# 🔍 Guía de Visualización Interactiva

## Comandos de Visualización Disponibles

### 1. **Visualización Básica (Incluida en generación)**
```bash
# Mostrar fractal al generarlo (quitar --no-show)
python main.py mandelbrot --preset high
python main.py julia --julia-c classic --colormap plasma
```

### 2. **Explorador Interactivo de Imagen Individual**
```bash
# Ver la última imagen generada con herramientas
python main.py explore

# Ver imagen específica con herramientas avanzadas
python main.py explore output/mandelbrot/imagen.png

# Modo interactivo completo con ventana grande
python main.py explore --interactive --figsize 16x12
```

**🔧 Herramientas disponibles:**
- **🔍 Zoom**: Botón de lupa en toolbar o rueda del ratón
- **👆 Pan**: Botón de mano para arrastrar la imagen
- **🏠 Home**: Resetear vista original
- **⬅️➡️ Back/Forward**: Navegar historial de zoom
- **⚙️ Configure**: Ajustar ejes, límites y vista
- **💾 Save**: Guardar vista actual en archivo
- **📊 Coordenadas**: Se muestran en tiempo real en la barra inferior

### 3. **Vista de Cuadrícula Multi-Fractal**
```bash
# Ver todos los fractales en cuadrícula 3x3
python main.py grid

# Cuadrícula personalizada de 2 columnas
python main.py grid --columns 2 --figsize 20x15

# Solo fractales Julia en cuadrícula
python main.py grid --fractal-type julia

# Solo fractales Mandelbrot
python main.py grid --fractal-type mandelbrot
```

**🎮 Características de la cuadrícula:**
- **Zoom independiente** en cada imagen
- **Comparación lado a lado** de diferentes fractales
- **Navegación con herramientas** estándar de matplotlib
- **Información de archivo** en cada imagen

### 4. **Galería HTML (Para navegación web)**
```bash
# Crear galería web con todas las imágenes
python main.py gallery

# Galería personalizada
python main.py gallery --output mi_galeria.html
```

**🌐 Características de la galería HTML:**
- **Vista web interactiva** con miniaturas
- **Modal de zoom** al hacer clic
- **Información de metadatos** para cada fractal
- **Navegación con teclado** (ESC para cerrar)

## 🎯 Casos de Uso Recomendados

### Para Exploración Detallada
```bash
# Generar fractal de alta calidad y explorarlo inmediatamente
python main.py mandelbrot --preset ultra --explore seahorse_valley --zoom 100
python main.py explore --interactive --figsize 20x15
```

### Para Comparación de Fractales
```bash
# Generar varios Julia sets y compararlos
python main.py julia --julia-c classic --no-show
python main.py julia --julia-c dragon --colormap inferno --no-show
python main.py julia --julia-c spiral --colormap plasma --no-show
python main.py grid --fractal-type julia
```

### Para Análisis de Detalles
```bash
# Generar fractal específico y analizar coordenadas
python main.py mandelbrot --zoom 200 --center-x -0.75 --center-y 0.1 --iterations 300
python main.py explore --interactive
# Usar herramientas de zoom para encontrar patrones interesantes
```

## 🔧 Consejos de Uso

### Navegación Eficiente
1. **Zoom inteligente**: Haz clic en un área y luego usa zoom para centrarte en esa región
2. **Historial de navegación**: Usa Back/Forward para comparar diferentes niveles de zoom
3. **Reset rápido**: Usa Home para volver a la vista completa instantáneamente

### Análisis de Patrones
1. **Coordenadas en tiempo real**: La barra inferior muestra la posición exacta del cursor
2. **Zoom progresivo**: Usa zoom gradual para descubrir detalles fractal por fractal
3. **Comparación directa**: La vista de cuadrícula permite comparar diferentes parámetros

### Guardado de Vistas
1. **Capturas específicas**: Usa el botón Save para guardar vistas interesantes
2. **Diferentes escalas**: Guarda la misma región en múltiples niveles de zoom
3. **Documentación visual**: Combina con metadatos para documentar hallazgos

## 💡 Comandos Útiles Combinados

```bash
# Workflow completo de exploración
python main.py mandelbrot --explore seahorse_valley --zoom 50 --preset high --no-show
python main.py mandelbrot --explore seahorse_valley --zoom 100 --preset high --no-show  
python main.py mandelbrot --explore seahorse_valley --zoom 200 --preset high --no-show
python main.py grid --fractal-type mandelbrot  # Ver serie completa
python main.py explore --interactive           # Explorar el más detallado

# Comparación de esquemas de colores
python main.py julia --julia-c classic --colormap hot --no-show
python main.py julia --julia-c classic --colormap plasma --no-show
python main.py julia --julia-c classic --colormap viridis --no-show
python main.py grid --fractal-type julia

# Análisis multi-resolución
python main.py mandelbrot --preset preview --zoom 10 --no-show
python main.py mandelbrot --preset standard --zoom 10 --no-show
python main.py mandelbrot --preset high --zoom 10 --no-show
python main.py grid --fractal-type mandelbrot
```

---

**🎯 Resultado**: Ahora tienes herramientas profesionales de visualización que rivalizan con software especializado, pero completamente integradas en tu generador de fractales!