"""
Generador de Fractales de Julia optimizado con Numba
==================================================

Este módulo implementa un algoritmo eficiente para generar fractales de Julia
usando compilación JIT para máximo rendimiento.

Los conjuntos de Julia se definen como:
z_{n+1} = z_n^2 + c

Donde z_0 = coordenada del píxel y c es una constante compleja fija.
Diferentes valores de c producen fractales únicos y fascinantes.
"""

import numpy as np
import matplotlib.pyplot as plt
from numba import jit
from typing import Tuple, Optional, Union
import time


@jit(nopython=True, fastmath=True)
def julia_point(z: complex, c: complex, max_iter: int) -> int:
    """
    Calcula el número de iteraciones antes de que z escape para un fractal de Julia.
    
    Args:
        z: Punto inicial (coordenada del píxel en el plano complejo)
        c: Constante compleja que define el conjunto de Julia específico
        max_iter: Número máximo de iteraciones
        
    Returns:
        Número de iteraciones antes del escape
    """
    for i in range(max_iter):
        if abs(z) > 2.0:  # Radio de escape
            return i
        z = z * z + c
    return max_iter


@jit(nopython=True, parallel=True, fastmath=True)
def julia_set(width: int, height: int, x_min: float, x_max: float,
              y_min: float, y_max: float, c_real: float, c_imag: float,
              max_iter: int) -> np.ndarray:
    """
    Genera la matriz completa del conjunto de Julia.
    
    Args:
        width, height: Dimensiones de la imagen
        x_min, x_max, y_min, y_max: Límites del plano complejo
        c_real, c_imag: Partes real e imaginaria de la constante c
        max_iter: Número máximo de iteraciones
        
    Returns:
        Matriz 2D con los valores de iteración para cada píxel
    """
    result = np.zeros((height, width), dtype=np.int32)
    c = complex(c_real, c_imag)
    
    # Calcular incrementos
    dx = (x_max - x_min) / width
    dy = (y_max - y_min) / height
    
    # Generar cada punto del fractal
    for y in range(height):
        for x in range(width):
            # Coordenada compleja inicial (z_0)
            real = x_min + x * dx
            imag = y_min + y * dy
            z = complex(real, imag)
            
            result[y, x] = julia_point(z, c, max_iter)
    
    return result


class JuliaGenerator:
    """
    Generador de fractales de Julia con presets y configuraciones avanzadas.
    """
    
    def __init__(self):
        """Inicializa con parámetros por defecto y presets famosos."""
        self.default_params = {
            'width': 800,
            'height': 600,
            'max_iter': 100,
            'x_center': 0.0,
            'y_center': 0.0,
            'zoom': 1.0,
            'colormap': 'plasma'
        }
        
        # Constantes c famosas que producen fractales hermosos
        self.famous_julia_sets = {
            'classic': -0.7 + 0.27015j,        # Julia clásico
            'dragon': -0.8 + 0.156j,           # Parecido a un dragón
            'spiral': -0.7 - 0.3j,             # Espirales
            'lightning': -0.54 + 0.54j,        # Rayos/relámpagos
            'dendrite': -0.235 + 0.85j,        # Estructura dendrítica
            'rabbit': -0.123 + 0.745j,         # Conejo de Douady
            'airplane': -0.75 + 0.1j,          # Forma de avión
            'galaxy': 0.285 + 0.01j,           # Estructura galáctica
            'flower': -0.4 + 0.6j,             # Pétalos florales
            'seahorse': -0.75 + 0.11j          # Caballito de mar
        }
    
    def parse_julia_c(self, c_input: Union[str, complex, Tuple[float, float]]) -> complex:
        """
        Convierte diferentes formatos de entrada a número complejo.
        
        Args:
            c_input: Puede ser:
                - String: "0.3+0.5i", "-0.7-0.27i", "classic", "dragon", etc.
                - Complex: Número complejo directo
                - Tuple: (parte_real, parte_imaginaria)
                
        Returns:
            Número complejo correspondiente
        """
        if isinstance(c_input, complex):
            return c_input
        elif isinstance(c_input, (tuple, list)) and len(c_input) == 2:
            return complex(c_input[0], c_input[1])
        elif isinstance(c_input, str):
            # Verificar si es un preset famoso
            if c_input.lower() in self.famous_julia_sets:
                return self.famous_julia_sets[c_input.lower()]
            
            # Parsear formato "a+bi" o "a-bi"
            c_input = c_input.replace('i', 'j').replace(' ', '')
            try:
                return complex(c_input)
            except ValueError:
                raise ValueError(f"Formato de c inválido: {c_input}. "
                               f"Use formatos como: '0.3+0.5j', 'classic', o tuple (0.3, 0.5)")
        else:
            raise ValueError(f"Tipo de entrada no soportado para c: {type(c_input)}")
    
    def calculate_bounds(self, x_center: float, y_center: float, zoom: float,
                        width: int, height: int) -> Tuple[float, float, float, float]:
        """Calcula los límites del plano complejo."""
        aspect_ratio = width / height
        base_extent = 4.0 / zoom
        
        x_extent = base_extent * aspect_ratio / 2
        y_extent = base_extent / 2
        
        return (
            x_center - x_extent,
            x_center + x_extent,
            y_center - y_extent,
            y_center + y_extent
        )
    
    def generate(self, julia_c: Union[str, complex, Tuple[float, float]] = 'classic',
                width: int = None, height: int = None, max_iter: int = None,
                x_center: float = None, y_center: float = None, zoom: float = None,
                colormap: str = None, verbose: bool = True) -> Tuple[np.ndarray, dict]:
        """
        Genera un fractal de Julia con los parámetros especificados.
        
        Args:
            julia_c: Constante c del fractal (string preset, complex, o tuple)
            Otros parámetros similares a MandelbrotGenerator
            
        Returns:
            Tupla (matriz_fractal, diccionario_parámetros_usados)
        """
        # Preparar parámetros
        params = self.default_params.copy()
        if width is not None: params['width'] = width
        if height is not None: params['height'] = height
        if max_iter is not None: params['max_iter'] = max_iter
        if x_center is not None: params['x_center'] = x_center
        if y_center is not None: params['y_center'] = y_center
        if zoom is not None: params['zoom'] = zoom
        if colormap is not None: params['colormap'] = colormap
        
        # Procesar constante c
        c = self.parse_julia_c(julia_c)
        params['julia_c'] = c
        
        if verbose:
            print(f"🌀 Generando Julia {params['width']}x{params['height']}")
            print(f"   Constante c: {c:.4f}")
            print(f"   Centro: ({params['x_center']:.3f}, {params['y_center']:.3f})")
            print(f"   Zoom: {params['zoom']:.2f}x, Iteraciones: {params['max_iter']}")
        
        # Calcular límites
        x_min, x_max, y_min, y_max = self.calculate_bounds(
            params['x_center'], params['y_center'], params['zoom'],
            params['width'], params['height']
        )
        
        # Cronometrar generación
        start_time = time.time()
        
        # Generar fractal
        fractal_data = julia_set(
            params['width'], params['height'],
            x_min, x_max, y_min, y_max,
            c.real, c.imag, params['max_iter']
        )
        
        elapsed = time.time() - start_time
        
        if verbose:
            pixels_per_second = (params['width'] * params['height']) / elapsed
            print(f"   ✅ Completado en {elapsed:.2f}s ({pixels_per_second:,.0f} píxeles/seg)")
        
        return fractal_data, params
    
    def plot(self, fractal_data: np.ndarray, params: dict,
             save_path: Optional[str] = None, show: bool = True) -> plt.Figure:
        """
        Visualiza el fractal de Julia generado.
        
        Args:
            fractal_data: Matriz del fractal
            params: Parámetros de generación
            save_path: Ruta de guardado opcional
            show: Si mostrar en pantalla
            
        Returns:
            Figura de matplotlib
        """
        fig, ax = plt.subplots(figsize=(12, 9), dpi=100)
        
        # Crear imagen
        extent = [
            params['x_center'] - 2/params['zoom'],
            params['x_center'] + 2/params['zoom'],
            params['y_center'] - 1.5/params['zoom'],
            params['y_center'] + 1.5/params['zoom']
        ]
        
        im = ax.imshow(fractal_data, extent=extent, cmap=params['colormap'],
                      origin='lower', interpolation='bilinear')
        
        # Título descriptivo
        c = params['julia_c']
        c_str = f"{c.real:.3f}{'+' if c.imag >= 0 else ''}{c.imag:.3f}i"
        ax.set_title(f"Fractal de Julia - c = {c_str}\n"
                    f"Centro: ({params['x_center']:.3f}, {params['y_center']:.3f}) | "
                    f"Zoom: {params['zoom']:.1f}x | Iteraciones: {params['max_iter']}", 
                    fontsize=14, pad=20)
        
        ax.set_xlabel('Parte Real', fontsize=12)
        ax.set_ylabel('Parte Imaginaria', fontsize=12)
        
        # Barra de colores
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Iteraciones hasta escape', rotation=270, labelpad=20)
        
        # Mejorar apariencia
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Guardar
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight',
                       facecolor='white', edgecolor='none')
            print(f"💾 Imagen guardada: {save_path}")
        
        if show:
            plt.show()
        
        return fig
    
    def generate_preset_gallery(self, output_dir: str = "output/julia_gallery/"):
        """
        Genera una galería con todos los presets famosos de Julia.
        
        Args:
            output_dir: Directorio donde guardar la galería
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"🎨 Generando galería de Julia sets en {output_dir}")
        
        for name, c_value in self.famous_julia_sets.items():
            print(f"   Generando '{name}'...")
            
            fractal, params = self.generate(
                julia_c=c_value, 
                width=800, 
                height=600, 
                max_iter=150,
                verbose=False
            )
            
            save_path = os.path.join(output_dir, f"julia_{name}.png")
            self.plot(fractal, params, save_path=save_path, show=False)
        
        print(f"✅ Galería completa: {len(self.famous_julia_sets)} fractales generados")


# Ejemplo de uso directo
if __name__ == "__main__":
    # Crear generador
    generator = JuliaGenerator()
    
    # Mostrar presets disponibles
    print("🌟 Presets disponibles:")
    for name, c in generator.famous_julia_sets.items():
        print(f"   {name}: c = {c}")
    
    # Generar un Julia clásico
    fractal, params = generator.generate('classic')
    generator.plot(fractal, params, save_path="output/julia_classic.png")