#!/usr/bin/env python3
"""
Generador de Arte Fractal - Script Principal
==========================================

Interfaz de línea de comandos para generar fractales de Mandelbrot y Julia
con opciones avanzadas de configuración y renderizado.

Uso:
    python main.py --help                    # Mostrar ayuda completa
    python main.py mandelbrot                # Mandelbrot básico
    python main.py julia --preset classic    # Julia clásico
    python main.py mandelbrot --zoom 100     # Mandelbrot con zoom
"""

import sys
import os
import click
import time
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mandelbrot import MandelbrotGenerator
from julia import JuliaGenerator
from config_manager import FractalConfig
from file_utils import FractalFileManager


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Mostrar versión del programa')
@click.pass_context
def cli(ctx, version):
    """
    🎨 Generador de Arte Fractal con IA
    
    Crea fractales matemáticamente hermosos usando algoritmos optimizados.
    Soporta fractales de Mandelbrot y Julia con múltiples opciones de personalización.
    """
    if version:
        click.echo("Generador de Arte Fractal v1.0.0")
        return
    
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.option('--width', '-w', default=None, type=int, help='Ancho de la imagen en píxeles')
@click.option('--height', '-h', default=None, type=int, help='Alto de la imagen en píxeles')
@click.option('--iterations', '-i', default=None, type=int, help='Número máximo de iteraciones')
@click.option('--zoom', '-z', default=None, type=float, help='Factor de zoom (mayor = más zoom)')
@click.option('--center-x', default=None, type=float, help='Coordenada X del centro')
@click.option('--center-y', default=None, type=float, help='Coordenada Y del centro')
@click.option('--colormap', '-c', default=None, help='Esquema de colores (hot, plasma, viridis, etc.)')
@click.option('--preset', '-p', default=None, help='Preset de calidad (preview, standard, high, ultra, print)')
@click.option('--output', '-o', default=None, help='Nombre del archivo de salida')
@click.option('--show/--no-show', default=True, help='Mostrar imagen al completar')
@click.option('--explore', default=None, help='Punto interesante a explorar (seahorse_valley, spiral, etc.)')
@click.option('--verbose/--quiet', default=True, help='Mostrar información detallada')
def mandelbrot(width, height, iterations, zoom, center_x, center_y, colormap, 
               preset, output, show, explore, verbose):
    """
    Genera un fractal de Mandelbrot.
    
    El conjunto de Mandelbrot es uno de los fractales más famosos,
    definido por la iteración z = z² + c donde c es la coordenada del píxel.
    
    Ejemplos:
        python main.py mandelbrot --preset high
        python main.py mandelbrot --zoom 100 --center-x -0.75 --center-y 0.1
        python main.py mandelbrot --explore seahorse_valley --zoom 50
    """
    try:
        # Cargar configuración
        config = FractalConfig()
        file_manager = FractalFileManager()
        
        # Aplicar preset si se especifica
        params = {}
        if preset:
            try:
                preset_params = config.get_quality_preset(preset)
                params.update(preset_params)
                if verbose:
                    click.echo(f"✅ Aplicando preset '{preset}': {preset_params}")
            except ValueError as e:
                click.echo(f"❌ Error: {e}", err=True)
                available_presets = config.list_available_presets()
                click.echo(f"Presets disponibles: {', '.join(available_presets)}")
                return
        
        # Aplicar punto de exploración si se especifica
        if explore:
            try:
                center_coords = config.get_interesting_point('mandelbrot', explore)
                center_x, center_y = center_coords
                if verbose:
                    click.echo(f"🎯 Explorando '{explore}': centro en ({center_x}, {center_y})")
            except ValueError as e:
                click.echo(f"❌ Error: {e}", err=True)
                available_points = config.list_interesting_points()
                click.echo(f"Puntos disponibles para Mandelbrot: {', '.join(available_points.get('mandelbrot', []))}")
                return
        
        # Aplicar parámetros de línea de comandos (sobrescriben preset)
        if width is not None: params['width'] = width
        if height is not None: params['height'] = height
        if iterations is not None: params['max_iter'] = iterations
        if zoom is not None: params['zoom'] = zoom
        if center_x is not None: params['x_center'] = center_x
        if center_y is not None: params['y_center'] = center_y
        if colormap is not None: params['colormap'] = colormap
        
        # Validar parámetros
        try:
            config.validate_parameters(params)
        except ValueError as e:
            click.echo(f"❌ Error de validación: {e}", err=True)
            return
        
        # Generar fractal
        if verbose:
            click.echo("🎨 Iniciando generación de Mandelbrot...")
        
        start_time = time.time()
        generator = MandelbrotGenerator()
        
        # Filtrar parámetros válidos para el generador
        generator_params = {k: v for k, v in params.items() 
                          if k in ['width', 'height', 'max_iter', 'x_center', 'y_center', 'zoom', 'colormap']}
        
        fractal_data, final_params = generator.generate(**generator_params, verbose=verbose)
        generation_time = time.time() - start_time
        
        # Guardar imagen
        if output:
            filename = output if output.endswith(('.png', '.jpg', '.jpeg')) else output + '.png'
        else:
            filename = None
        
        # Obtener DPI del preset o usar por defecto
        dpi = params.get('dpi', 150)
        
        save_path = file_manager.save_fractal_image(
            fractal_data, final_params, filename, 
            save_metadata=True, create_thumbnail=True, dpi=dpi
        )
        
        # Mostrar estadísticas
        if verbose:
            pixels = final_params['width'] * final_params['height']
            click.echo(f"⚡ Rendimiento: {pixels/generation_time:,.0f} píxeles/segundo")
            click.echo(f"📁 Archivo guardado: {save_path}")
        
        # Mostrar imagen si se solicita
        if show:
            generator.plot(fractal_data, final_params, show=True)
        
    except Exception as e:
        click.echo(f"❌ Error inesperado: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()


@cli.command()
@click.option('--julia-c', '-c', default='classic', help='Constante c del Julia set (classic, dragon, spiral, etc. o formato "a+bi")')
@click.option('--width', '-w', default=None, type=int, help='Ancho de la imagen en píxeles')
@click.option('--height', '-h', default=None, type=int, help='Alto de la imagen en píxeles')
@click.option('--iterations', '-i', default=None, type=int, help='Número máximo de iteraciones')
@click.option('--zoom', '-z', default=None, type=float, help='Factor de zoom')
@click.option('--center-x', default=None, type=float, help='Coordenada X del centro')
@click.option('--center-y', default=None, type=float, help='Coordenada Y del centro')
@click.option('--colormap', default=None, help='Esquema de colores')
@click.option('--preset', '-p', default=None, help='Preset de calidad')
@click.option('--output', '-o', default=None, help='Nombre del archivo de salida')
@click.option('--show/--no-show', default=True, help='Mostrar imagen al completar')
@click.option('--gallery', is_flag=True, help='Generar galería con todos los presets famosos')
@click.option('--verbose/--quiet', default=True, help='Mostrar información detallada')
def julia(julia_c, width, height, iterations, zoom, center_x, center_y, colormap,
          preset, output, show, gallery, verbose):
    """
    Genera un fractal de Julia.
    
    Los conjuntos de Julia son fractales relacionados con Mandelbrot,
    definidos por z = z² + c donde c es una constante fija.
    
    Ejemplos:
        python main.py julia --julia-c classic
        python main.py julia --julia-c "0.3+0.5i" --preset high
        python main.py julia --julia-c dragon --zoom 2
        python main.py julia --gallery
    """
    try:
        # Cargar configuración
        config = FractalConfig()
        file_manager = FractalFileManager()
        generator = JuliaGenerator()
        
        # Generar galería si se solicita
        if gallery:
            if verbose:
                click.echo("🎨 Generando galería completa de Julia sets...")
            
            gallery_dir = "output/julia_gallery"
            generator.generate_preset_gallery(gallery_dir)
            
            # Crear galería HTML
            file_manager.create_gallery_html("julia_gallery.html")
            click.echo(f"✅ Galería completa generada en {gallery_dir}")
            return
        
        # Aplicar preset si se especifica
        params = {}
        if preset:
            try:
                preset_params = config.get_quality_preset(preset)
                params.update(preset_params)
                if verbose:
                    click.echo(f"✅ Aplicando preset '{preset}': {preset_params}")
            except ValueError as e:
                click.echo(f"❌ Error: {e}", err=True)
                return
        
        # Aplicar parámetros de línea de comandos
        if width is not None: params['width'] = width
        if height is not None: params['height'] = height
        if iterations is not None: params['max_iter'] = iterations
        if zoom is not None: params['zoom'] = zoom
        if center_x is not None: params['x_center'] = center_x
        if center_y is not None: params['y_center'] = center_y
        if colormap is not None: params['colormap'] = colormap
        
        # Validar parámetros
        try:
            config.validate_parameters(params)
        except ValueError as e:
            click.echo(f"❌ Error de validación: {e}", err=True)
            return
        
        # Generar fractal
        if verbose:
            click.echo(f"🌀 Iniciando generación de Julia con c = {julia_c}...")
        
        start_time = time.time()
        
        # Filtrar parámetros válidos para el generador
        generator_params = {k: v for k, v in params.items() 
                          if k in ['width', 'height', 'max_iter', 'x_center', 'y_center', 'zoom', 'colormap']}
        
        fractal_data, final_params = generator.generate(
            julia_c=julia_c, **generator_params, verbose=verbose
        )
        generation_time = time.time() - start_time
        
        # Guardar imagen
        if output:
            filename = output if output.endswith(('.png', '.jpg', '.jpeg')) else output + '.png'
        else:
            filename = None
        
        # Obtener DPI del preset o usar por defecto
        dpi = params.get('dpi', 150)
        
        save_path = file_manager.save_fractal_image(
            fractal_data, final_params, filename,
            save_metadata=True, create_thumbnail=True, dpi=dpi
        )
        
        # Mostrar estadísticas
        if verbose:
            pixels = final_params['width'] * final_params['height']
            click.echo(f"⚡ Rendimiento: {pixels/generation_time:,.0f} píxeles/segundo")
            click.echo(f"📁 Archivo guardado: {save_path}")
        
        # Mostrar imagen si se solicita
        if show:
            generator.plot(fractal_data, final_params, show=True)
        
    except Exception as e:
        click.echo(f"❌ Error inesperado: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()


@cli.command()
def info():
    """
    Muestra información del sistema y configuración disponible.
    """
    try:
        config = FractalConfig()
        file_manager = FractalFileManager()
        
        click.echo("📊 Información del Generador de Arte Fractal")
        click.echo("=" * 50)
        
        # Presets disponibles
        click.echo("\n🎯 Presets de Calidad:")
        for preset in config.list_available_presets():
            params = config.get_quality_preset(preset)
            click.echo(f"   {preset:8}: {params['width']:4}x{params['height']:<4} "
                      f"({params['max_iter']:3} iter, {params['dpi']} DPI)")
        
        # Colormaps disponibles
        click.echo("\n🎨 Esquemas de Colores:")
        for category in ['warm', 'cool', 'artistic', 'classic']:
            maps = config.get_colormap_category(category)
            click.echo(f"   {category:9}: {', '.join(maps)}")
        
        # Puntos interesantes
        click.echo("\n🎯 Puntos de Exploración:")
        interesting_points = config.list_interesting_points()
        for fractal_type, points in interesting_points.items():
            click.echo(f"   {fractal_type:9}: {', '.join(points)}")
        
        # Julia presets
        generator = JuliaGenerator()
        click.echo("\n🌀 Presets de Julia:")
        for name, c_value in generator.famous_julia_sets.items():
            click.echo(f"   {name:12}: c = {c_value}")
        
        # Estadísticas de archivos
        click.echo("\n📁 Estadísticas de Almacenamiento:")
        stats = file_manager.get_storage_stats()
        click.echo(f"   Total imágenes: {stats['total_images']}")
        click.echo(f"   Mandelbrot:     {stats['mandelbrot_count']}")
        click.echo(f"   Julia:          {stats['julia_count']}")
        click.echo(f"   Tamaño total:   {stats['total_size_mb']:.1f} MB")
        click.echo(f"   Miniaturas:     {stats['thumbnails_count']}")
        click.echo(f"   Metadatos:      {stats['metadata_files']}")
        
    except Exception as e:
        click.echo(f"❌ Error obteniendo información: {e}", err=True)


@cli.command()
@click.option('--output', '-o', default=None, help='Nombre del archivo HTML de galería')
def gallery(output):
    """
    Genera una galería HTML con todas las imágenes creadas.
    """
    try:
        file_manager = FractalFileManager()
        
        click.echo("🌐 Generando galería HTML...")
        gallery_path = file_manager.create_gallery_html(output)
        
        stats = file_manager.get_storage_stats()
        click.echo(f"✅ Galería creada: {gallery_path}")
        click.echo(f"   Imágenes incluidas: {stats['total_images']}")
        
        # Sugerir cómo abrir
        click.echo(f"\n💡 Para ver la galería, abre: {gallery_path}")
        
    except Exception as e:
        click.echo(f"❌ Error creando galería: {e}", err=True)


@cli.command()
@click.argument('image_path', required=False)
@click.option('--interactive', '-i', is_flag=True, help='Modo interactivo con herramientas de zoom')
@click.option('--figsize', default='12x9', help='Tamaño de figura (ej: 12x9, 16x12)')
def explore(image_path, interactive, figsize):
    """
    Abre imágenes fractal con herramientas interactivas de zoom y exploración.
    
    Si no se especifica imagen, muestra la última generada.
    Incluye herramientas de matplotlib: zoom, pan, configuración, guardado.
    
    Ejemplos:
        python main.py explore                                    # Última imagen
        python main.py explore output/mandelbrot/imagen.png       # Imagen específica
        python main.py explore --interactive --figsize 16x12      # Modo interactivo grande
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        from pathlib import Path
        import numpy as np
        
        # Si no se especifica imagen, buscar la más reciente
        if not image_path:
            output_dir = Path("output")
            image_files = []
            for subdir in ["mandelbrot", "julia"]:
                subdir_path = output_dir / subdir
                if subdir_path.exists():
                    for ext in ["*.png", "*.jpg", "*.jpeg"]:
                        image_files.extend(subdir_path.glob(ext))
            
            if not image_files:
                click.echo("❌ No se encontraron imágenes. Genera algunas primero:")
                click.echo("   python main.py mandelbrot")
                return
            
            # Usar la más reciente
            image_path = str(max(image_files, key=lambda p: p.stat().st_mtime))
            click.echo(f"📸 Abriendo imagen más reciente: {Path(image_path).name}")
        
        # Verificar que existe
        if not Path(image_path).exists():
            click.echo(f"❌ Archivo no encontrado: {image_path}")
            return
        
        # Parsear tamaño de figura
        try:
            width, height = map(int, figsize.split('x'))
        except:
            width, height = 12, 9
            click.echo(f"⚠️  Formato de figsize inválido, usando {width}x{height}")
        
        # Configurar matplotlib para modo interactivo
        plt.ion()  # Interactive mode ON
        
        # Crear figura con herramientas
        fig = plt.figure(figsize=(width, height))
        fig.canvas.manager.set_window_title('🔍 Explorador de Fractales - Herramientas Disponibles')
        
        # Cargar y mostrar imagen
        img = mpimg.imread(image_path)
        plt.imshow(img)
        plt.axis('on')  # Mostrar ejes para referencia
        
        # Título informativo
        plt.title(f'🎨 {Path(image_path).name}\n'
                 f'🔍 Herramientas: Zoom | Pan | Home | Back/Forward | Configure | Save', 
                 fontsize=12, pad=20)
        
        # Mostrar información sobre herramientas
        click.echo("\n🔧 Herramientas disponibles en la ventana:")
        click.echo("   🔍 Zoom: Botón de lupa o rueda del ratón")
        click.echo("   👆 Pan: Botón de mano para arrastrar")
        click.echo("   🏠 Home: Resetear vista")
        click.echo("   ⬅️➡️ Back/Forward: Navegar historial de zoom")
        click.echo("   ⚙️  Configure: Ajustar ejes y vista")
        click.echo("   💾 Save: Guardar vista actual")
        click.echo("   📊 Coordenadas: Se muestran en la barra inferior")
        
        if interactive:
            click.echo("\n🎮 Modo interactivo activado:")
            click.echo("   - Haz clic y arrastra para hacer pan")
            click.echo("   - Usa la rueda del ratón para zoom")
            click.echo("   - Presiona 'q' o cierra la ventana para salir")
            
            # Conectar eventos del ratón para información adicional
            def on_click(event):
                if event.inaxes:
                    click.echo(f"📍 Click en: ({event.xdata:.1f}, {event.ydata:.1f})")
            
            fig.canvas.mpl_connect('button_press_event', on_click)
        
        # Activar toolbar completo
        fig.canvas.toolbar_visible = True
        
        # Mostrar y mantener ventana abierta
        plt.tight_layout()
        plt.show(block=True)  # Bloquear hasta que se cierre la ventana
        
        click.echo("✅ Exploración completada")
        
    except ImportError as e:
        click.echo(f"❌ Error de importación: {e}")
        click.echo("   Instala las dependencias: pip install matplotlib")
    except Exception as e:
        click.echo(f"❌ Error abriendo imagen: {e}")


@cli.command()
@click.option('--columns', '-c', default=3, help='Número de columnas en la cuadrícula')
@click.option('--figsize', default='15x10', help='Tamaño de la figura completa')
@click.option('--fractal-type', type=click.Choice(['all', 'mandelbrot', 'julia']), default='all', help='Tipo de fractales a mostrar')
def grid(columns, figsize, fractal_type):
    """
    Muestra múltiples fractales en una cuadrícula interactiva.
    
    Permite comparar diferentes fractales lado a lado con herramientas de zoom.
    
    Ejemplos:
        python main.py grid                              # Todos los fractales en cuadrícula 3x3
        python main.py grid --columns 2 --figsize 20x15 # Cuadrícula 2 columnas, figura grande
        python main.py grid --fractal-type julia        # Solo fractales Julia
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg
        from pathlib import Path
        import math
        
        # Buscar imágenes según el tipo
        output_dir = Path("output")
        image_files = []
        
        search_dirs = []
        if fractal_type == 'all':
            search_dirs = ["mandelbrot", "julia"]
        else:
            search_dirs = [fractal_type]
        
        for subdir in search_dirs:
            subdir_path = output_dir / subdir
            if subdir_path.exists():
                for ext in ["*.png", "*.jpg", "*.jpeg"]:
                    image_files.extend(subdir_path.glob(ext))
        
        if not image_files:
            click.echo(f"❌ No se encontraron imágenes de tipo '{fractal_type}'")
            click.echo("   Genera algunas primero:")
            click.echo("   python main.py mandelbrot")
            click.echo("   python main.py julia --julia-c classic")
            return
        
        # Ordenar por fecha de modificación (más recientes primero)
        image_files = sorted(image_files, key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Calcular disposición de la cuadrícula
        num_images = len(image_files)
        rows = math.ceil(num_images / columns)
        
        # Parsear tamaño de figura
        try:
            width, height = map(int, figsize.split('x'))
        except:
            width, height = 15, 10
        
        click.echo(f"🖼️  Mostrando {num_images} imágenes en cuadrícula {columns}x{rows}")
        
        # Configurar matplotlib
        plt.ion()
        fig, axes = plt.subplots(rows, columns, figsize=(width, height))
        fig.canvas.manager.set_window_title('🎨 Galería de Fractales - Vista Cuadrícula')
        
        # Mostrar cada imagen
        for i, img_path in enumerate(image_files):
            if i >= rows * columns:
                break
                
            if rows == 1 and columns == 1:
                ax = axes
            elif rows == 1 or columns == 1:
                ax = axes[i] if i < len(axes) else None
            else:
                ax = axes[i // columns, i % columns] if i < rows * columns else None
            
            if ax is None:
                continue
                
            try:
                img = mpimg.imread(str(img_path))
                ax.imshow(img)
                ax.set_title(img_path.name, fontsize=8, pad=5)
                ax.axis('off')
            except Exception as e:
                ax.text(0.5, 0.5, f'Error cargando\n{img_path.name}', 
                       ha='center', va='center', transform=ax.transAxes)
                ax.axis('off')
        
        # Ocultar ejes vacíos
        total_subplots = rows * columns
        for i in range(num_images, total_subplots):
            if rows == 1 and columns == 1:
                continue
            elif rows == 1 or columns == 1:
                if i < len(axes):
                    axes[i].axis('off')
            else:
                row, col = i // columns, i % columns
                if row < rows and col < columns:
                    axes[row, col].axis('off')
        
        # Configurar figura
        plt.suptitle(f'🎨 Galería de Fractales ({fractal_type.title()})\n'
                    f'🔍 Usa las herramientas para hacer zoom en cualquier imagen', 
                    fontsize=14, y=0.98)
        
        plt.tight_layout()
        fig.canvas.toolbar_visible = True
        
        # Información para el usuario
        click.echo("\n🔧 Herramientas de navegación disponibles:")
        click.echo("   🔍 Zoom: Selecciona una imagen y usa zoom")
        click.echo("   👆 Pan: Arrastra para mover la vista")
        click.echo("   🏠 Home: Resetear vista completa")
        click.echo("   💾 Save: Guardar vista actual")
        click.echo("\n💡 Haz clic en cualquier imagen y usa zoom para explorar detalles")
        
        plt.show(block=True)
        click.echo("✅ Vista de cuadrícula cerrada")
        
    except ImportError as e:
        click.echo(f"❌ Error de importación: {e}")
    except Exception as e:
        click.echo(f"❌ Error creando cuadrícula: {e}")


@cli.command()
def clean():
    """
    Limpia archivos temporales y reorganiza el directorio de salida.
    """
    try:
        file_manager = FractalFileManager()
        
        # Mostrar estadísticas antes
        stats_before = file_manager.get_storage_stats()
        click.echo(f"📊 Archivos actuales: {stats_before['total_images']} imágenes")
        
        # Aquí podrías implementar lógica de limpieza
        # Por ahora, solo mostramos la información
        click.echo("🧹 Funcionalidad de limpieza no implementada aún")
        click.echo("   (Reservado para futuras versiones)")
        
    except Exception as e:
        click.echo(f"❌ Error en limpieza: {e}", err=True)


if __name__ == "__main__":
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("src"):
        click.echo("❌ Error: Ejecute este script desde el directorio raíz del proyecto", err=True)
        click.echo("   (donde se encuentra la carpeta 'src')")
        sys.exit(1)
    
    cli()