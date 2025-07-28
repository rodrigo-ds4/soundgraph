#!/usr/bin/env python3
"""
🚀 LAUNCHER - SoundGraph Desktop
==============================
Script simple para ejecutar la aplicación de escritorio
"""

import sys
import os

def main():
    print("🎵 Iniciando SoundGraph Desktop...")
    print("=" * 50)
    
    try:
        # Importar y ejecutar la aplicación
        from soundgraph_desktop import SoundGraphDesktop
        
        print("✅ Módulos cargados correctamente")
        print("🏔️ Abriendo interfaz gráfica...")
        
        # Crear y ejecutar aplicación
        app = SoundGraphDesktop()
        app.run()
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("\n💡 Soluciones:")
        print("   1. Activar entorno virtual: source venv/bin/activate")
        print("   2. Instalar dependencias: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error ejecutando aplicación: {e}")
        print("\n🔍 Verifica que:")
        print("   • PyVista esté instalado correctamente")
        print("   • Tu sistema tenga soporte para ventanas gráficas")
        
    finally:
        print("\n👋 ¡Gracias por usar SoundGraph!")

if __name__ == "__main__":
    main() 