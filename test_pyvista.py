#!/usr/bin/env python3
"""
🧪 TEST PYVISTA - Verificar funcionalidad 3D
============================================
Test simple para verificar que PyVista funciona correctamente
"""

import numpy as np
import pyvista as pv

def test_pyvista_basic():
    """Test básico de PyVista"""
    print("🧪 TESTING PYVISTA...")
    print("=" * 30)
    
    try:
        # 1. Verificar importación
        print("✅ PyVista importado correctamente")
        print(f"   Versión: {pv.__version__}")
        
        # 2. Crear datos de prueba (superficie musical simulada)
        print("\n🎵 Creando superficie de prueba...")
        
        # Simular un paisaje sonoro simple
        x = np.linspace(0, 60, 100)  # 60 segundos
        y = np.array([0, 1, 2])      # 3 bandas (graves, medios, agudos)
        X, Y = np.meshgrid(x, y)
        
        # Crear "montañas" simuladas de música
        Z = (np.sin(X/10) + np.cos(X/15) + 
             np.sin(Y*3) * 0.5 + 
             np.random.random(X.shape) * 0.2)
        
        print(f"   Superficie: {Z.shape[0]} bandas × {Z.shape[1]} frames")
        
        # 3. Crear mesh
        print("🔧 Creando mesh 3D...")
        mesh = pv.StructuredGrid(X, Y, Z)
        mesh['intensity'] = Z.ravel()
        
        # 4. Configurar visualización
        print("🎨 Configurando visualización...")
        pv.set_plot_theme("dark")
        
        plotter = pv.Plotter(
            window_size=[1200, 800],
            title="🧪 Test PyVista - Superficie Musical Simulada"
        )
        
        # Agregar superficie
        plotter.add_mesh(
            mesh,
            scalars='intensity',
            cmap='plasma',
            opacity=0.9,
            smooth_shading=True,
            show_scalar_bar=True,
            scalar_bar_args={'title': 'Intensidad', 'color': 'white'}
        )
        
        # Etiquetas de prueba
        plotter.add_text(
            "🕐 TIEMPO (simulado)",
            position='lower_left',
            font_size=14,
            color='cyan'
        )
        
        plotter.add_text(
            "🎵 GRAVES → MEDIOS → AGUDOS",
            position='lower_right',
            font_size=12,
            color='orange'
        )
        
        plotter.add_text(
            "🧪 TEST PYVISTA\n✅ Si ves esta ventana, PyVista funciona!",
            position='upper_left',
            font_size=14,
            color='white'
        )
        
        # Controles
        plotter.add_text(
            "🖱️ CONTROLES:\n• Arrastrar: Rotar\n• Scroll: Zoom\n• 'q': Cerrar",
            position='upper_right',
            font_size=12,
            color='lightgray'
        )
        
        # Configurar cámara
        plotter.camera_position = 'iso'
        
        print("✨ Abriendo ventana de prueba...")
        print("\n🎮 Si ves la ventana 3D, ¡PyVista funciona correctamente!")
        print("   Usa el mouse para navegar, 'q' para cerrar")
        
        # Mostrar ventana
        plotter.show(interactive_update=True)
        
        print("\n🎉 ¡TEST COMPLETADO!")
        print("   PyVista está funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST:")
        print(f"   {str(e)}")
        return False

def main():
    """Ejecutar test"""
    print("🎵 SOUNDGRAPH - Test PyVista")
    print("=" * 40)
    
    success = test_pyvista_basic()
    
    if success:
        print("\n✅ PyVista está listo para usar!")
        print("   Puedes ejecutar: python soundgraph_simple.py")
    else:
        print("\n❌ Hay problemas con PyVista")
        print("💡 Posibles soluciones:")
        print("   • Reinstalar: pip install pyvista --upgrade")
        print("   • Verificar dependencias gráficas del sistema")
        print("   • En macOS: instalar XQuartz si es necesario")

if __name__ == "__main__":
    main() 