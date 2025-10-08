"""
Utilidades de Guardado y Gestión de Archivos
==========================================

Este módulo proporciona funciones para guardar, organizar y gestionar
las imágenes generadas por el generador de fractales, incluyendo
metadatos, thumbnails y organización automática.
"""

import os
import json
import yaml
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import hashlib


class FractalFileManager:
    """
    Administrador de archivos para imágenes de fractales generadas.
    
    Características:
    - Guardado con metadatos completos
    - Generación automática de thumbnails
    - Organización por fecha y tipo
    - Prevención de duplicados
    - Gestión de galería
    """
    
    def __init__(self, base_output_dir: str = "output"):
        """
        Inicializa el administrador de archivos.
        
        Args:
            base_output_dir: Directorio base donde guardar archivos
        """
        self.base_output_dir = Path(base_output_dir)
        self.ensure_directories()
    
    def ensure_directories(self):
        """Crea la estructura de directorios necesaria."""
        directories = [
            self.base_output_dir,
            self.base_output_dir / "mandelbrot",
            self.base_output_dir / "julia", 
            self.base_output_dir / "thumbnails",
            self.base_output_dir / "metadata",
            self.base_output_dir / "gallery"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def generate_unique_filename(self, fractal_type: str, params: Dict[str, Any],
                                extension: str = "png") -> str:
        """
        Genera un nombre de archivo único basado en parámetros.
        
        Args:
            fractal_type: Tipo de fractal (mandelbrot, julia)
            params: Parámetros del fractal
            extension: Extensión del archivo
            
        Returns:
            Nombre de archivo único
        """
        # Crear hash de parámetros relevantes para evitar duplicados
        param_str = f"{fractal_type}_{params.get('width', 800)}x{params.get('height', 600)}"
        param_str += f"_iter{params.get('max_iter', 100)}"
        param_str += f"_zoom{params.get('zoom', 1.0):.3f}"
        param_str += f"_center{params.get('x_center', 0.0):.6f},{params.get('y_center', 0.0):.6f}"
        
        if fractal_type == 'julia' and 'julia_c' in params:
            c = params['julia_c']
            param_str += f"_c{c.real:.6f},{c.imag:.6f}"
        
        # Crear hash corto para evitar nombres muy largos
        param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
        
        # Timestamp para unicidad
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"{fractal_type}_{timestamp}_{param_hash}.{extension}"
        return filename
    
    def save_fractal_image(self, fractal_data: np.ndarray, params: Dict[str, Any],
                          filename: Optional[str] = None, save_metadata: bool = True,
                          create_thumbnail: bool = True, dpi: int = 150) -> str:
        """
        Guarda una imagen de fractal con todas las opciones.
        
        Args:
            fractal_data: Matriz de datos del fractal
            params: Parámetros de generación
            filename: Nombre personalizado (se genera automáticamente si es None)
            save_metadata: Si guardar archivo de metadatos
            create_thumbnail: Si crear miniatura
            dpi: DPI para la imagen guardada
            
        Returns:
            Ruta completa del archivo guardado
        """
        # Determinar tipo de fractal
        fractal_type = "julia" if "julia_c" in params else "mandelbrot"
        
        # Generar nombre de archivo si no se proporciona
        if filename is None:
            filename = self.generate_unique_filename(fractal_type, params)
        
        # Crear ruta completa
        subdir = self.base_output_dir / fractal_type
        filepath = subdir / filename
        
        # Crear figura para guardar con configuración simple
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Configurar imagen
        extent = self._calculate_extent(params)
        im = ax.imshow(fractal_data, extent=extent, cmap=params.get('colormap', 'hot'),
                      origin='lower', interpolation='bilinear')
        
        # Configurar título y etiquetas con tamaños de fuente seguros
        title = self._generate_title(fractal_type, params)
        ax.set_title(title, fontsize=12, pad=15)
        ax.set_xlabel('Parte Real', fontsize=10)
        ax.set_ylabel('Parte Imaginaria', fontsize=10)
        
        # Barra de colores
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Iteraciones hasta escape', rotation=270, labelpad=15, fontsize=9)
        
        # Mejorar apariencia sin tight_layout
        ax.grid(True, alpha=0.3)
        
        # Guardar imagen con DPI seguro
        safe_dpi = min(dpi, 150)  # Limitar aún más el DPI
        plt.savefig(str(filepath), dpi=safe_dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        plt.close(fig)
        
        print(f"💾 Imagen guardada: {filepath}")
        
        # Guardar metadatos si se solicita
        if save_metadata:
            self.save_metadata(filepath, params, fractal_data.shape)
        
        # Crear miniatura si se solicita
        if create_thumbnail:
            self.create_thumbnail(filepath)
        
        return str(filepath)
    
    def _calculate_extent(self, params: Dict[str, Any]) -> List[float]:
        """Calcula la extensión del plano complejo para la imagen."""
        zoom = params.get('zoom', 1.0)
        x_center = params.get('x_center', 0.0)
        y_center = params.get('y_center', 0.0)
        
        x_range = 4.0 / zoom
        y_range = 3.0 / zoom
        
        return [
            x_center - x_range/2,
            x_center + x_range/2,
            y_center - y_range/2,
            y_center + y_range/2
        ]
    
    def _generate_title(self, fractal_type: str, params: Dict[str, Any]) -> str:
        """Genera título descriptivo para la imagen."""
        if fractal_type == "julia":
            c = params.get('julia_c', 0+0j)
            c_str = f"{c.real:.3f}{'+' if c.imag >= 0 else ''}{c.imag:.3f}i"
            title = f"Fractal de Julia - c = {c_str}"
        else:
            title = f"Fractal de Mandelbrot - Zoom {params.get('zoom', 1.0):.1f}x"
        
        title += f"\nCentro: ({params.get('x_center', 0.0):.4f}, {params.get('y_center', 0.0):.4f})"
        title += f" | Iteraciones: {params.get('max_iter', 100)}"
        
        return title
    
    def save_metadata(self, image_path: str, params: Dict[str, Any], 
                     data_shape: Tuple[int, int]):
        """
        Guarda metadatos detallados del fractal.
        
        Args:
            image_path: Ruta de la imagen guardada
            params: Parámetros de generación
            data_shape: Dimensiones de la matriz de datos
        """
        # Preparar metadatos
        metadata = {
            'generation_info': {
                'timestamp': datetime.datetime.now().isoformat(),
                'image_path': str(image_path),
                'data_shape': list(data_shape),
                'total_pixels': data_shape[0] * data_shape[1]
            },
            'fractal_parameters': params.copy(),
            'technical_info': {
                'algorithm': 'escape_time',
                'escape_radius': 2.0,
                'optimization': 'numba_jit'
            }
        }
        
        # Convertir números complejos a formato serializable
        if 'julia_c' in metadata['fractal_parameters']:
            c = metadata['fractal_parameters']['julia_c']
            metadata['fractal_parameters']['julia_c'] = {
                'real': float(c.real),
                'imag': float(c.imag),
                'string': f"{c.real:.6f}{'+' if c.imag >= 0 else ''}{c.imag:.6f}i"
            }
        
        # Guardar como YAML (más legible)
        metadata_path = self.base_output_dir / "metadata" / (Path(image_path).stem + "_metadata.yaml")
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            yaml.dump(metadata, f, default_flow_style=False, allow_unicode=True)
        
        print(f"📋 Metadatos guardados: {metadata_path}")
    
    def create_thumbnail(self, image_path: str, thumbnail_size: Tuple[int, int] = (200, 150)):
        """
        Crea una miniatura de la imagen.
        
        Args:
            image_path: Ruta de la imagen original
            thumbnail_size: Tamaño de la miniatura (ancho, alto)
        """
        try:
            # Abrir imagen original
            with Image.open(image_path) as img:
                # Crear miniatura manteniendo aspecto
                img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
                
                # Guardar miniatura
                thumbnail_path = self.base_output_dir / "thumbnails" / (Path(image_path).stem + "_thumb.png")
                img.save(thumbnail_path, "PNG", optimize=True)
                
                print(f"🖼️  Miniatura creada: {thumbnail_path}")
                
        except Exception as e:
            print(f"❌ Error creando miniatura: {e}")
    
    def create_gallery_html(self, output_file: str = None) -> str:
        """
        Genera una galería HTML con todas las imágenes.
        
        Args:
            output_file: Nombre del archivo HTML (se genera automáticamente si es None)
            
        Returns:
            Ruta del archivo HTML generado
        """
        if output_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"fractal_gallery_{timestamp}.html"
        
        gallery_path = self.base_output_dir / "gallery" / output_file
        
        # Buscar todas las imágenes
        image_files = []
        for subdir in ["mandelbrot", "julia"]:
            subdir_path = self.base_output_dir / subdir
            if subdir_path.exists():
                for ext in ["*.png", "*.jpg", "*.jpeg"]:
                    image_files.extend(subdir_path.glob(ext))
        
        # Generar HTML
        html_content = self._generate_gallery_html(image_files)
        
        # Guardar archivo
        with open(gallery_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 Galería HTML creada: {gallery_path}")
        print(f"   Imágenes incluidas: {len(image_files)}")
        
        return str(gallery_path)
    
    def _generate_gallery_html(self, image_files: List[Path]) -> str:
        """Genera el contenido HTML para la galería."""
        html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galería de Arte Fractal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f0f0; }
        .header { text-align: center; margin-bottom: 30px; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .fractal-card { background: white; border-radius: 10px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .fractal-image { width: 100%; height: auto; border-radius: 5px; cursor: pointer; }
        .fractal-info { margin-top: 10px; font-size: 14px; color: #666; }
        .fractal-title { font-weight: bold; color: #333; margin-bottom: 5px; }
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); }
        .modal-content { margin: auto; display: block; width: 80%; max-width: 1200px; }
        .close { position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 Galería de Arte Fractal</h1>
        <p>Generado el """ + datetime.datetime.now().strftime("%d/%m/%Y a las %H:%M") + """</p>
    </div>
    
    <div class="gallery">
"""
        
        # Agregar cada imagen
        for img_path in sorted(image_files):
            # Intentar cargar metadatos
            metadata_path = self.base_output_dir / "metadata" / (img_path.stem + "_metadata.yaml")
            metadata = {}
            
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r', encoding='utf-8') as f:
                        metadata = yaml.safe_load(f)
                except:
                    pass
            
            # Información de la imagen
            fractal_type = "Julia" if "julia" in img_path.name.lower() else "Mandelbrot"
            relative_path = os.path.relpath(img_path, self.base_output_dir)
            
            params = metadata.get('fractal_parameters', {})
            zoom = params.get('zoom', 'N/A')
            iterations = params.get('max_iter', 'N/A')
            
            html += f"""
        <div class="fractal-card">
            <img class="fractal-image" src="../{relative_path}" alt="{fractal_type} Fractal" onclick="openModal(this.src)">
            <div class="fractal-title">{fractal_type} Fractal</div>
            <div class="fractal-info">
                Zoom: {zoom}x<br>
                Iteraciones: {iterations}<br>
                Archivo: {img_path.name}
            </div>
        </div>
"""
        
        html += """
    </div>
    
    <!-- Modal para imagen ampliada -->
    <div id="imageModal" class="modal" onclick="closeModal()">
        <span class="close">&times;</span>
        <img class="modal-content" id="modalImage">
    </div>
    
    <script>
        function openModal(src) {
            document.getElementById('imageModal').style.display = 'block';
            document.getElementById('modalImage').src = src;
        }
        
        function closeModal() {
            document.getElementById('imageModal').style.display = 'none';
        }
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') closeModal();
        });
    </script>
</body>
</html>
"""
        
        return html
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de almacenamiento."""
        stats = {
            'total_images': 0,
            'mandelbrot_count': 0,
            'julia_count': 0,
            'total_size_mb': 0,
            'thumbnails_count': 0,
            'metadata_files': 0
        }
        
        # Contar archivos y calcular tamaño
        for subdir in ["mandelbrot", "julia"]:
            subdir_path = self.base_output_dir / subdir
            if subdir_path.exists():
                for ext in ["*.png", "*.jpg", "*.jpeg"]:
                    files = list(subdir_path.glob(ext))
                    stats['total_images'] += len(files)
                    
                    if subdir == "mandelbrot":
                        stats['mandelbrot_count'] += len(files)
                    else:
                        stats['julia_count'] += len(files)
                    
                    # Calcular tamaño total
                    for file in files:
                        stats['total_size_mb'] += file.stat().st_size / (1024 * 1024)
        
        # Contar miniaturas
        thumbs_dir = self.base_output_dir / "thumbnails"
        if thumbs_dir.exists():
            stats['thumbnails_count'] = len(list(thumbs_dir.glob("*.png")))
        
        # Contar metadatos
        metadata_dir = self.base_output_dir / "metadata"
        if metadata_dir.exists():
            stats['metadata_files'] = len(list(metadata_dir.glob("*.yaml")))
        
        return stats


# Ejemplo de uso
if __name__ == "__main__":
    # Crear administrador de archivos
    file_manager = FractalFileManager()
    
    # Mostrar estadísticas
    stats = file_manager.get_storage_stats()
    print("📊 Estadísticas de almacenamiento:")
    print(f"   Total de imágenes: {stats['total_images']}")
    print(f"   Mandelbrot: {stats['mandelbrot_count']}")
    print(f"   Julia: {stats['julia_count']}")
    print(f"   Tamaño total: {stats['total_size_mb']:.1f} MB")
    print(f"   Miniaturas: {stats['thumbnails_count']}")
    print(f"   Archivos de metadatos: {stats['metadata_files']}")
    
    # Crear galería si hay imágenes
    if stats['total_images'] > 0:
        gallery_path = file_manager.create_gallery_html()
        print(f"\n🌐 Galería disponible en: {gallery_path}")