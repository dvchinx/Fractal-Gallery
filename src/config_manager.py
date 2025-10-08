"""
Sistema de Configuración para el Generador de Arte Fractal
========================================================

Este módulo maneja la carga, validación y gestión de configuraciones
para el generador de fractales, incluyendo presets de calidad,
esquemas de colores, y parámetros de renderizado.
"""

import yaml
import os
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import datetime


class FractalConfig:
    """
    Administrador de configuración centralizado para el generador de fractales.
    
    Características:
    - Carga configuración desde YAML
    - Presets de calidad predefinidos
    - Validación de parámetros
    - Gestión de rutas de salida
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa el sistema de configuración.
        
        Args:
            config_path: Ruta al archivo de configuración YAML
        """
        self.config_path = config_path or self._find_config_file()
        self.config = self._load_config()
        
    def _find_config_file(self) -> str:
        """Busca el archivo de configuración en ubicaciones estándar."""
        possible_paths = [
            "config/fractal_config.yaml",
            "../config/fractal_config.yaml",
            os.path.join(os.path.dirname(__file__), "../config/fractal_config.yaml")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        raise FileNotFoundError("No se encontró archivo de configuración fractal_config.yaml")
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo YAML."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                print(f"✅ Configuración cargada desde: {self.config_path}")
                return config
        except Exception as e:
            print(f"❌ Error cargando configuración: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Configuración mínima por defecto si no se puede cargar el archivo."""
        return {
            'rendering': {
                'default_width': 800,
                'default_height': 600,
                'default_max_iter': 100,
                'default_dpi': 100,
                'image_format': 'png'
            },
            'exploration': {
                'default_zoom': 1.0,
                'max_zoom': 1000.0
            },
            'colormaps': {
                'warm': ['hot', 'plasma'],
                'cool': ['viridis', 'cool'],
                'artistic': ['rainbow', 'hsv'],
                'classic': ['gray', 'bone']
            },
            'output': {
                'filename_template': '{type}_{preset}_{timestamp}',
                'timestamp_format': '%Y%m%d_%H%M%S'
            }
        }
    
    def get_quality_preset(self, preset_name: str) -> Dict[str, Any]:
        """
        Obtiene los parámetros para un preset de calidad específico.
        
        Args:
            preset_name: Nombre del preset (preview, standard, high, ultra, print)
            
        Returns:
            Diccionario con parámetros de renderizado
        """
        presets = self.config.get('quality_presets', {})
        
        if preset_name not in presets:
            available = list(presets.keys())
            raise ValueError(f"Preset '{preset_name}' no encontrado. "
                           f"Disponibles: {available}")
        
        return presets[preset_name].copy()
    
    def get_colormap_category(self, category: str) -> List[str]:
        """
        Obtiene lista de colormaps para una categoría específica.
        
        Args:
            category: Categoría de colormap (warm, cool, artistic, classic)
            
        Returns:
            Lista de nombres de colormaps
        """
        colormaps = self.config.get('colormaps', {})
        
        if category not in colormaps:
            available = list(colormaps.keys())
            raise ValueError(f"Categoría '{category}' no encontrada. "
                           f"Disponibles: {available}")
        
        return colormaps[category].copy()
    
    def get_all_colormaps(self) -> List[str]:
        """Obtiene todos los colormaps disponibles en una lista plana."""
        all_maps = []
        for category_maps in self.config.get('colormaps', {}).values():
            all_maps.extend(category_maps)
        return list(set(all_maps))  # Eliminar duplicados
    
    def get_interesting_point(self, fractal_type: str, point_name: str) -> Tuple[float, float]:
        """
        Obtiene coordenadas de un punto interesante para exploración.
        
        Args:
            fractal_type: Tipo de fractal (mandelbrot, julia)
            point_name: Nombre del punto interesante
            
        Returns:
            Tupla (x, y) con las coordenadas
        """
        points = self.config.get('exploration', {}).get('interesting_points', {})
        
        if fractal_type not in points:
            available_types = list(points.keys())
            raise ValueError(f"Tipo '{fractal_type}' no encontrado. "
                           f"Disponibles: {available_types}")
        
        type_points = points[fractal_type]
        if point_name not in type_points:
            available_points = list(type_points.keys())
            raise ValueError(f"Punto '{point_name}' no encontrado para {fractal_type}. "
                           f"Disponibles: {available_points}")
        
        coords = type_points[point_name]
        return tuple(coords)
    
    def generate_filename(self, fractal_type: str, preset: str = "custom",
                         extension: Optional[str] = None) -> str:
        """
        Genera un nombre de archivo siguiendo el template configurado.
        
        Args:
            fractal_type: Tipo de fractal (mandelbrot, julia)
            preset: Nombre del preset usado
            extension: Extensión del archivo (se usa la configurada si no se especifica)
            
        Returns:
            Nombre de archivo generado
        """
        output_config = self.config.get('output', {})
        template = output_config.get('filename_template', '{type}_{preset}_{timestamp}')
        timestamp_format = output_config.get('timestamp_format', '%Y%m%d_%H%M%S')
        
        # Generar timestamp
        timestamp = datetime.datetime.now().strftime(timestamp_format)
        
        # Aplicar template
        filename = template.format(
            type=fractal_type,
            preset=preset,
            timestamp=timestamp
        )
        
        # Agregar extensión
        if extension is None:
            extension = self.config.get('rendering', {}).get('image_format', 'png')
        
        if not extension.startswith('.'):
            extension = '.' + extension
            
        return filename + extension
    
    def get_output_path(self, filename: str, base_dir: str = "output") -> str:
        """
        Genera la ruta completa de salida con organización automática.
        
        Args:
            filename: Nombre del archivo
            base_dir: Directorio base de salida
            
        Returns:
            Ruta completa donde guardar el archivo
        """
        output_config = self.config.get('output', {})
        path_parts = [base_dir]
        
        # Organizar por fecha si está habilitado
        if output_config.get('organize_by_date', False):
            today = datetime.datetime.now().strftime('%Y-%m-%d')
            path_parts.append(today)
        
        # Organizar por tipo si está habilitado
        if output_config.get('organize_by_type', False):
            # Extraer tipo del nombre de archivo
            if filename.startswith('mandelbrot'):
                path_parts.append('mandelbrot')
            elif filename.startswith('julia'):
                path_parts.append('julia')
            else:
                path_parts.append('other')
        
        # Crear directorio si no existe
        directory = os.path.join(*path_parts)
        os.makedirs(directory, exist_ok=True)
        
        return os.path.join(directory, filename)
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """
        Valida parámetros de renderizado contra límites de configuración.
        
        Args:
            params: Diccionario de parámetros a validar
            
        Returns:
            True si todos los parámetros son válidos
            
        Raises:
            ValueError: Si algún parámetro está fuera de límites
        """
        algorithms = self.config.get('algorithms', {})
        
        # Validar límites de iteraciones
        max_iter_limit = algorithms.get('max_iterations_limit', 1000)
        if params.get('max_iter', 0) > max_iter_limit:
            raise ValueError(f"max_iter ({params['max_iter']}) excede el límite "
                           f"de {max_iter_limit}")
        
        # Validar límites de resolución
        max_res_limit = algorithms.get('max_resolution_limit', 8192)
        width = params.get('width', 0)
        height = params.get('height', 0)
        
        if width > max_res_limit or height > max_res_limit:
            raise ValueError(f"Resolución ({width}x{height}) excede el límite "
                           f"de {max_res_limit}px")
        
        # Advertir sobre uso alto de memoria
        cli_config = self.config.get('cli', {})
        if cli_config.get('warn_on_high_memory', True):
            memory_threshold = cli_config.get('memory_warning_threshold', 1000000000)
            estimated_memory = width * height * 4 * 2  # Aproximación conservadora
            
            if estimated_memory > memory_threshold:
                memory_gb = estimated_memory / (1024**3)
                print(f"⚠️  Advertencia: Uso estimado de memoria: {memory_gb:.1f} GB")
        
        return True
    
    def get_rendering_defaults(self) -> Dict[str, Any]:
        """Obtiene los valores por defecto para renderizado."""
        return self.config.get('rendering', {}).copy()
    
    def list_available_presets(self) -> List[str]:
        """Lista todos los presets de calidad disponibles."""
        return list(self.config.get('quality_presets', {}).keys())
    
    def list_interesting_points(self) -> Dict[str, List[str]]:
        """Lista todos los puntos interesantes organizados por tipo."""
        points = self.config.get('exploration', {}).get('interesting_points', {})
        return {ftype: list(points_dict.keys()) 
                for ftype, points_dict in points.items()}


# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia de configuración
    config = FractalConfig()
    
    # Mostrar presets disponibles
    print("📋 Presets de calidad disponibles:")
    for preset in config.list_available_presets():
        params = config.get_quality_preset(preset)
        print(f"   {preset}: {params['width']}x{params['height']}, "
              f"{params['max_iter']} iter")
    
    # Mostrar colormaps
    print(f"\n🎨 Colormaps disponibles: {len(config.get_all_colormaps())} total")
    for category in ['warm', 'cool', 'artistic', 'classic']:
        maps = config.get_colormap_category(category)
        print(f"   {category}: {', '.join(maps)}")
    
    # Generar nombre de archivo de ejemplo
    filename = config.generate_filename('mandelbrot', 'high')
    output_path = config.get_output_path(filename)
    print(f"\n📁 Ejemplo de ruta: {output_path}")