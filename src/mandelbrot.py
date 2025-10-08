"""
Generador de Fractales de Mandelbrot optimizado con Numba
=======================================================

Este módulo implementa un algoritmo eficiente para generar fractales de Mandelbrot
usando compilación JIT (Just In Time) con Numba para máximo rendimiento.

El conjunto de Mandelbrot se define como:
z_{n+1} = z_n^2 + c

Donde z_0 = 0 y c es un número complejo que corresponde a cada pixel de la imagen.
"""

import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from typing import Tuple, Optional
import time


@jit(nopython=True, fastmath=True)
def mandelbrot_point(c: complex, max_iter: int) -> int:
    """
    Calcula el número de iteraciones antes de que z escape para un punto c dado.
    
    Args:
        c: Número complejo que representa el punto en el plano complejo
        max_iter: Número máximo de iteraciones antes de considerar que el punto está en el conjunto
        
    Returns:
        Número de iteraciones antes del escape (max_iter si no escapa)
    """
    z = 0.0 + 0.0j
    for i in range(max_iter):
        if abs(z) > 2.0:  # Radio de escape estándar
            return i
        z = z * z + c
    return max_iter


@jit(nopython=True, parallel=True, fastmath=True)
def mandelbrot_set(width: int, height: int, x_min: float, x_max: float, 
                   y_min: float, y_max: float, max_iter: int) -> np.ndarray:
    """
    Genera la matriz completa del conjunto de Mandelbrot.
    
    Args:
        width: Ancho de la imagen en píxeles
        height: Alto de la imagen en píxeles
        x_min, x_max: Rango del eje real (X)
        y_min, y_max: Rango del eje imaginario (Y)
        max_iter: Número máximo de iteraciones por punto
        
    Returns:
        Matriz 2D con los valores de iteración para cada píxel
    """
    # Crear matriz de resultados
    result = np.zeros((height, width), dtype=np.int32)
    
    # Calcular incrementos para cada píxel
    dx = (x_max - x_min) / width
    dy = (y_max - y_min) / height
    
    # Paralelización automática con Numba
    for y in range(height):
        for x in range(width):
            # Convertir coordenadas de píxel a coordenadas complejas
            real = x_min + x * dx
            imag = y_min + y * dy
            c = complex(real, imag)
            
            # Calcular iteraciones para este punto
            result[y, x] = mandelbrot_point(c, max_iter)
    
    return result


class MandelbrotGenerator:
    """
    Generador de fractales de Mandelbrot con opciones avanzadas de configuración.
    """
    
    def __init__(self):
        """Inicializa el generador con valores por defecto."""
        self.default_params = {
            'width': 800,
            'height': 600,
            'max_iter': 100,
            'x_center': -0.5,
            'y_center': 0.0,
            'zoom': 1.0,
            'colormap': 'hot'
        }
    
    def calculate_bounds(self, x_center: float, y_center: float, zoom: float, 
                        width: int, height: int) -> Tuple[float, float, float, float]:
        """
        Calcula los límites del plano complejo basado en centro, zoom y aspecto.
        
        Args:
            x_center, y_center: Coordenadas del centro
            zoom: Factor de zoom (mayor = más zoom)
            width, height: Dimensiones de la imagen
            
        Returns:
            Tupla (x_min, x_max, y_min, y_max)
        """
        # Mantener aspecto correcto
        aspect_ratio = width / height
        
        # Calcular extensión base (viewport sin zoom)
        base_extent = 4.0 / zoom  # El conjunto estándar abarca ~4 unidades
        
        x_extent = base_extent * aspect_ratio / 2
        y_extent = base_extent / 2
        
        return (
            x_center - x_extent,
            x_center + x_extent,
            y_center - y_extent,
            y_center + y_extent
        )
    
    def generate(self, width: int = None, height: int = None, max_iter: int = None,
                x_center: float = None, y_center: float = None, zoom: float = None,
                colormap: str = None, verbose: bool = True) -> Tuple[np.ndarray, dict]:
        """
        Genera un fractal de Mandelbrot con los parámetros especificados.
        
        Args:
            width, height: Resolución de la imagen
            max_iter: Número máximo de iteraciones
            x_center, y_center: Centro del fractal
            zoom: Factor de zoom
            colormap: Esquema de colores de matplotlib
            verbose: Si mostrar información de progreso
            
        Returns:
            Tupla (matriz_fractal, diccionario_parámetros_usados)
        """
        # Usar valores por defecto si no se especifican
        params = self.default_params.copy()
        if width is not None: params['width'] = width
        if height is not None: params['height'] = height
        if max_iter is not None: params['max_iter'] = max_iter
        if x_center is not None: params['x_center'] = x_center
        if y_center is not None: params['y_center'] = y_center
        if zoom is not None: params['zoom'] = zoom
        if colormap is not None: params['colormap'] = colormap
        
        if verbose:
            print(f"🎨 Generando Mandelbrot {params['width']}x{params['height']}")
            print(f"   Centro: ({params['x_center']:.4f}, {params['y_center']:.4f})")
            print(f"   Zoom: {params['zoom']:.2f}x, Iteraciones: {params['max_iter']}")
        
        # Calcular límites del viewport
        x_min, x_max, y_min, y_max = self.calculate_bounds(
            params['x_center'], params['y_center'], params['zoom'],
            params['width'], params['height']
        )
        
        # Cronometrar la generación
        start_time = time.time()
        
        # Generar el fractal (aquí es donde Numba acelera dramáticamente)
        fractal_data = mandelbrot_set(
            params['width'], params['height'],
            x_min, x_max, y_min, y_max,
            params['max_iter']
        )
        
        elapsed = time.time() - start_time
        
        if verbose:
            pixels_per_second = (params['width'] * params['height']) / elapsed
            print(f"   ✅ Completado en {elapsed:.2f}s ({pixels_per_second:,.0f} píxeles/seg)")
        
        return fractal_data, params
    
    def plot(self, fractal_data: np.ndarray, params: dict, 
             save_path: Optional[str] = None, show: bool = True) -> plt.Figure:
        """
        Visualiza el fractal generado con colores y etiquetas.
        
        Args:
            fractal_data: Matriz del fractal generada
            params: Parámetros usados en la generación
            save_path: Ruta donde guardar la imagen (opcional)
            show: Si mostrar la imagen en pantalla
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
        
        # Crear imagen con colormap
        im = ax.imshow(fractal_data, extent=[
            params['x_center'] - 2/params['zoom'],
            params['x_center'] + 2/params['zoom'],
            params['y_center'] - 1.5/params['zoom'], 
            params['y_center'] + 1.5/params['zoom']
        ], cmap=params['colormap'], origin='lower', interpolation='bilinear')
        
        # Configurar título y etiquetas
        ax.set_title(f"Fractal de Mandelbrot - Zoom {params['zoom']:.1f}x\n"
                    f"Centro: ({params['x_center']:.4f}, {params['y_center']:.4f}) | "
                    f"Iteraciones: {params['max_iter']}", fontsize=14, pad=20)
        ax.set_xlabel('Parte Real', fontsize=12)
        ax.set_ylabel('Parte Imaginaria', fontsize=12)
        
        # Barra de colores
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Iteraciones hasta escape', rotation=270, labelpad=20)
        
        # Mejorar apariencia
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Guardar si se especifica ruta
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            print(f"💾 Imagen guardada: {save_path}")
        
        if show:
            plt.show()
        
        return fig


# Ejemplo de uso directo del módulo
if __name__ == "__main__":
    # Crear generador
    generator = MandelbrotGenerator()
    
    # Generar fractal básico
    fractal, params = generator.generate()
    
    # Visualizar
    generator.plot(fractal, params, save_path="output/mandelbrot_basic.png")