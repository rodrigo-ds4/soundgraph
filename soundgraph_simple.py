#!/usr/bin/env python3
"""
🎵 SOUNDGRAPH SIMPLE - Consola + Ventana 3D
==========================================
Versión minimalista: consola + PyVista 3D directo
- Input por terminal
- Análisis automático
- Ventana 3D pura
"""

import os
import sys
import numpy as np
import pyvista as pv
from audio_journey_3d import AudioJourney3D

def print_banner():
    """Mostrar banner de inicio"""
    print("\n" + "="*60)
    print("🎵 SOUNDGRAPH SIMPLE - Análisis 3D de Audio")
    print("="*60)
    print("🏔️ Explora tu música como un paisaje sonoro")
    print("🎵 Graves | 🎶 Medios | 🎵 Agudos")
    print("="*60 + "\n")

def select_audio_file():
    """Seleccionar archivo de audio por consola"""
    print("📁 SELECCIÓN DE ARCHIVO:")
    print("-" * 25)
    
    while True:
        file_path = input("🎧 Ingresa la ruta del archivo de audio: ").strip()
        
        # Remover comillas si las hay
        file_path = file_path.strip('"\'')
        
        if not file_path:
            continue
            
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            continue
            
        # Verificar extensión
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in ['.wav', '.mp3', '.m4a', '.flac']:
            print(f"⚠️  Formato no soportado: {ext}")
            print("   Formatos válidos: .wav, .mp3, .m4a, .flac")
            continue
            
        print(f"✅ Archivo seleccionado: {os.path.basename(file_path)}")
        return file_path

def get_duration():
    """Obtener duración a analizar"""
    print("\n⏱️  DURACIÓN A ANALIZAR:")
    print("-" * 24)
    
    while True:
        try:
            duration = input("🕐 Minutos a analizar (0.5-5.0) [default: 1.0]: ").strip()
            
            if not duration:
                return 1.0
                
            duration = float(duration)
            
            if 0.5 <= duration <= 5.0:
                print(f"✅ Analizando {duration} minutos")
                return duration
            else:
                print("❌ Duración debe estar entre 0.5 y 5.0 minutos")
                
        except ValueError:
            print("❌ Ingresa un número válido")

def analyze_audio(file_path, duration):
    """Analizar archivo de audio"""
    print(f"\n🔬 INICIANDO ANÁLISIS:")
    print("-" * 22)
    print(f"📄 Archivo: {os.path.basename(file_path)}")
    print(f"⏱️  Duración: {duration} minutos")
    print(f"🎵 Separando graves, medios y agudos...")
    
    # Crear motor de análisis
    engine = AudioJourney3D()
    
    print("🔊 Procesando audio...")
    result = engine.process_full_journey(file_path, duration_minutes=duration)
    
    if result['success']:
        print("\n🎉 ¡ANÁLISIS COMPLETADO!")
        print("-" * 23)
        print(f"⏱️  Duración procesada: {result['duration']:.1f}s")
        print(f"📊 Frames temporales: {result['journey_stats']['total_frames']}")
        print(f"🎵 Bandas de frecuencia: {result['journey_stats']['freq_bands']}")
        print(f"🔍 Puntos de malla: {result['journey_stats']['mesh_points']}")
        return result
    else:
        print(f"\n❌ ERROR EN ANÁLISIS:")
        print(f"   {result['error']}")
        return None

def create_3d_visualization(journey_data):
    """Crear y mostrar visualización 3D"""
    print(f"\n🏔️  CREANDO PAISAJE 3D:")
    print("-" * 24)
    
    try:
        # Obtener datos
        pyvista_data = journey_data['pyvista_data']
        landscape = pyvista_data['landscape']
        time_frames = pyvista_data['time_frames']
        band_names = pyvista_data['band_names']
        
        print(f"🌊 Superficie: {landscape.shape[0]} bandas × {landscape.shape[1]} frames")
        print(f"🎵 Bandas: {', '.join(band_names).upper()}")
        
        # Configurar PyVista tema oscuro
        pv.set_plot_theme("dark")
        
        # Crear plotter
        plotter = pv.Plotter(
            window_size=[1600, 1000],
            title="🏔️ SoundGraph 3D - Paisaje Sonoro Interactivo"
        )
        
        # Crear coordenadas de malla
        x_coords = time_frames
        y_coords = np.arange(len(band_names))
        X, Y = np.meshgrid(x_coords, y_coords)
        Z = landscape
        
        # Crear superficie
        mesh = pv.StructuredGrid(X, Y, Z)
        mesh['intensity'] = Z.ravel()
        
        print("🎨 Aplicando colores y texturas...")
        
        # Agregar superficie con colores vibrantes
        plotter.add_mesh(
            mesh,
            scalars='intensity',
            cmap='plasma',  # Colormap musical
            opacity=0.9,
            smooth_shading=True,
            show_scalar_bar=True,
            scalar_bar_args={
                'title': '🔊 INTENSIDAD SONORA',
                'color': 'white',
                'title_font_size': 16,
                'label_font_size': 12,
                'position_x': 0.85,
                'position_y': 0.1
            }
        )
        
        # Agregar etiquetas descriptivas
        plotter.add_text(
            "🕐 TIEMPO (segundos)",
            position='lower_left',
            font_size=16,
            color='cyan'
        )
        
        plotter.add_text(
            f"🎵 FRECUENCIAS: {' → '.join(band_names).upper()}",
            position='lower_right',
            font_size=14,
            color='orange'
        )
        
        plotter.add_text(
            f"🏔️ PAISAJE SONORO 3D\n"
            f"📊 {landscape.shape[1]} frames × {landscape.shape[0]} bandas\n"
            f"⏱️ {time_frames[-1]:.1f} segundos de música",
            position='upper_left',
            font_size=14,
            color='white'
        )
        
        # Agregar instrucciones
        plotter.add_text(
            "🖱️ CONTROLES:\n"
            "• Arrastrar: Rotar vista\n"
            "• Scroll: Zoom in/out\n"
            "• Click derecho: Pan\n"
            "• 'r': Reset vista\n"
            "• 'q': Salir",
            position='upper_right',
            font_size=12,
            color='lightgray'
        )
        
        # Configurar cámara óptima
        plotter.camera_position = 'iso'
        plotter.camera.azimuth = 45
        plotter.camera.elevation = 30
        
        # Iluminación avanzada
        plotter.enable_shadows()
        plotter.add_light(pv.Light(position=(10, 10, 10), focal_point=(0, 0, 0), color='white'))
        
        print("✨ Abriendo ventana 3D...")
        print("\n🎮 CONTROLES DE NAVEGACIÓN:")
        print("   🖱️  Mouse: Rotar vista")
        print("   🔄 Scroll: Zoom")
        print("   🖱️  Click derecho: Pan")
        print("   ⌨️  'r': Reset vista")
        print("   ⌨️  'q': Cerrar ventana")
        print("\n🏔️ ¡Explora tu paisaje sonoro!")
        
        # Mostrar ventana 3D (bloquea hasta cerrar)
        plotter.show(interactive_update=True)
        
        print("\n👋 Ventana 3D cerrada.")
        
    except Exception as e:
        print(f"\n❌ ERROR CREANDO 3D:")
        print(f"   {str(e)}")

def main():
    """Función principal"""
    try:
        # Banner de inicio
        print_banner()
        
        # 1. Seleccionar archivo
        file_path = select_audio_file()
        
        # 2. Configurar duración
        duration = get_duration()
        
        # 3. Analizar audio
        result = analyze_audio(file_path, duration)
        
        if not result:
            print("\n❌ No se pudo completar el análisis.")
            return
        
        # 4. Crear visualización 3D
        create_3d_visualization(result)
        
        print("\n🎉 ¡Sesión completada!")
        print("   Gracias por usar SoundGraph Simple")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operación cancelada por el usuario.")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO:")
        print(f"   {str(e)}")
        print("\n💡 Verifica que:")
        print("   • PyVista esté instalado")
        print("   • El archivo de audio sea válido")
        print("   • Tengas suficiente memoria RAM")

if __name__ == "__main__":
    main() 