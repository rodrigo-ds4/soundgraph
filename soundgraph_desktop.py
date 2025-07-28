"""
🎵 SOUNDGRAPH DESKTOP - Aplicación Nativa 3D 🏔️
================================================
Aplicación de escritorio con PyVista para visualización 3D avanzada
- Interfaz nativa con tkinter
- PyVista 3D interactivo en ventana separada
- Análisis completo de graves, medios y agudos
- Navegación temporal fluida
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
from audio_journey_3d import AudioJourney3D
import pyvista as pv
import numpy as np

class SoundGraphDesktop:
    def __init__(self):
        """Inicializar aplicación de escritorio"""
        self.root = tk.Tk()
        self.root.title("🎵 SoundGraph Desktop - Viaje 3D por tu Música")
        self.root.geometry("800x600")
        self.root.configure(bg='#1a1a1a')
        
        # Variables
        self.current_file = None
        self.journey_data = None
        self.plotter = None
        
        # Configurar PyVista para escritorio
        pv.set_plot_theme("dark")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        
        # Título principal
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🎵 SoundGraph Desktop",
            font=("Arial", 24, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Explora tu música en 3D - Separación de Graves, Medios y Agudos",
            font=("Arial", 12),
            fg='#cccccc',
            bg='#1a1a1a'
        )
        subtitle_label.pack()
        
        # Frame de carga de archivo
        file_frame = tk.Frame(self.root, bg='#2a2a2a', padx=20, pady=20)
        file_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            file_frame,
            text="📁 Seleccionar Archivo de Audio:",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        ).pack(anchor='w')
        
        # Frame de botones de archivo
        button_frame = tk.Frame(file_frame, bg='#2a2a2a')
        button_frame.pack(fill='x', pady=10)
        
        self.select_button = tk.Button(
            button_frame,
            text="🎧 Seleccionar Audio",
            command=self.select_file,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.select_button.pack(side='left')
        
        self.file_label = tk.Label(
            button_frame,
            text="Ningún archivo seleccionado",
            font=("Arial", 10),
            fg='#cccccc',
            bg='#2a2a2a'
        )
        self.file_label.pack(side='left', padx=(20, 0))
        
        # Frame de análisis
        analysis_frame = tk.Frame(self.root, bg='#2a2a2a', padx=20, pady=20)
        analysis_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            analysis_frame,
            text="🔬 Análisis de Audio:",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        ).pack(anchor='w')
        
        # Configuración de duración
        duration_frame = tk.Frame(analysis_frame, bg='#2a2a2a')
        duration_frame.pack(fill='x', pady=10)
        
        tk.Label(
            duration_frame,
            text="⏱️ Duración a analizar (minutos):",
            font=("Arial", 11),
            fg='#ffffff',
            bg='#2a2a2a'
        ).pack(side='left')
        
        self.duration_var = tk.DoubleVar(value=1.0)
        self.duration_scale = tk.Scale(
            duration_frame,
            from_=0.5,
            to=5.0,
            resolution=0.5,
            orient='horizontal',
            variable=self.duration_var,
            bg='#3a3a3a',
            fg='#ffffff',
            highlightbackground='#2a2a2a'
        )
        self.duration_scale.pack(side='left', padx=(10, 0))
        
        # Botón de análisis
        self.analyze_button = tk.Button(
            analysis_frame,
            text="🚀 Generar Viaje 3D",
            command=self.start_analysis,
            font=("Arial", 14, "bold"),
            bg='#FF6B35',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            state='disabled'
        )
        self.analyze_button.pack(pady=20)
        
        # Barra de progreso
        self.progress_frame = tk.Frame(analysis_frame, bg='#2a2a2a')
        self.progress_frame.pack(fill='x', pady=10)
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Arial", 10),
            fg='#cccccc',
            bg='#2a2a2a'
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill='x', pady=5)
        
        # Frame de resultados
        results_frame = tk.Frame(self.root, bg='#2a2a2a', padx=20, pady=20)
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(
            results_frame,
            text="📊 Resultados:",
            font=("Arial", 14, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        ).pack(anchor='w')
        
        # Área de resultados
        self.results_text = tk.Text(
            results_frame,
            height=8,
            bg='#1a1a1a',
            fg='#cccccc',
            font=("Courier", 10),
            padx=10,
            pady=10
        )
        self.results_text.pack(fill='both', expand=True, pady=10)
        
        # Botones de visualización
        viz_frame = tk.Frame(results_frame, bg='#2a2a2a')
        viz_frame.pack(fill='x', pady=10)
        
        self.viz3d_button = tk.Button(
            viz_frame,
            text="🏔️ Abrir Visualización 3D",
            command=self.open_3d_visualization,
            font=("Arial", 12, "bold"),
            bg='#9C27B0',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.viz3d_button.pack(side='left')
        
        self.export_button = tk.Button(
            viz_frame,
            text="💾 Exportar Datos",
            command=self.export_html,
            font=("Arial", 12, "bold"),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.export_button.pack(side='left', padx=(10, 0))
        
    def select_file(self):
        """Seleccionar archivo de audio"""
        file_types = [
            ("Archivos de Audio", "*.wav *.mp3 *.m4a *.flac"),
            ("WAV files", "*.wav"),
            ("MP3 files", "*.mp3"),
            ("M4A files", "*.m4a"),
            ("FLAC files", "*.flac"),
            ("Todos los archivos", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=file_types
        )
        
        if file_path:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"📄 {filename}")
            self.analyze_button.config(state='normal')
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"✅ Archivo cargado: {filename}\n")
            self.results_text.insert(tk.END, f"📍 Ruta: {file_path}\n\n")
            
    def start_analysis(self):
        """Iniciar análisis en hilo separado"""
        if not self.current_file:
            messagebox.showerror("Error", "Selecciona un archivo primero")
            return
            
        # Deshabilitar botones
        self.analyze_button.config(state='disabled')
        self.viz3d_button.config(state='disabled')
        self.export_button.config(state='disabled')
        
        # Mostrar progreso
        self.progress_label.config(text="🎵 Analizando audio...")
        self.progress_bar.start()
        
        # Ejecutar análisis en hilo separado
        threading.Thread(target=self.analyze_audio, daemon=True).start()
        
    def analyze_audio(self):
        """Análizar audio (ejecuta en hilo separado)"""
        try:
            duration = self.duration_var.get()
            
            # Actualizar UI desde hilo
            self.root.after(0, lambda: self.progress_label.config(text="🔊 Separando frecuencias..."))
            
            # Crear motor de análisis
            engine = AudioJourney3D()
            
            # Procesar audio
            result = engine.process_full_journey(self.current_file, duration_minutes=duration)
            
            # Actualizar UI con resultados
            self.root.after(0, lambda: self.analysis_complete(result))
            
        except Exception as e:
            self.root.after(0, lambda: self.analysis_error(str(e)))
            
    def analysis_complete(self, result):
        """Análisis completado"""
        self.progress_bar.stop()
        self.progress_label.config(text="")
        
        if result['success']:
            self.journey_data = result
            
            # Mostrar resultados
            self.results_text.insert(tk.END, "🎉 ¡Análisis completado!\n\n")
            self.results_text.insert(tk.END, f"⏱️ Duración analizada: {result['duration']:.1f} segundos\n")
            self.results_text.insert(tk.END, f"📊 Frames temporales: {result['journey_stats']['total_frames']}\n")
            self.results_text.insert(tk.END, f"🎵 Bandas de frecuencia: {result['journey_stats']['freq_bands']}\n")
            self.results_text.insert(tk.END, f"🔍 Puntos de malla: {result['journey_stats']['mesh_points']}\n\n")
            self.results_text.insert(tk.END, "🏔️ ¡Paisaje 3D generado! Haz clic en 'Abrir Visualización 3D'\n")
            
            # Habilitar botones
            self.viz3d_button.config(state='normal')
            self.export_button.config(state='normal')
            
        else:
            self.results_text.insert(tk.END, f"❌ Error: {result['error']}\n")
            
        self.analyze_button.config(state='normal')
        
    def analysis_error(self, error):
        """Error en análisis"""
        self.progress_bar.stop()
        self.progress_label.config(text="")
        
        self.results_text.insert(tk.END, f"❌ Error durante el análisis:\n{error}\n\n")
        self.analyze_button.config(state='normal')
        
        messagebox.showerror("Error de Análisis", f"Error procesando audio:\n{error}")
        
    def open_3d_visualization(self):
        """Abrir visualización 3D con PyVista"""
        if not self.journey_data:
            messagebox.showerror("Error", "No hay datos para visualizar")
            return
            
        try:
            # Obtener datos 3D generados
            pyvista_data = self.journey_data['pyvista_data']
            landscape = pyvista_data['landscape']
            time_frames = pyvista_data['time_frames']
            band_names = pyvista_data['band_names']
            
            # Crear plotter de PyVista
            self.plotter = pv.Plotter(
                window_size=[1400, 900],
                title="🏔️ SoundGraph 3D - Paisaje Sonoro Interactivo"
            )
            
            # Crear coordenadas para la malla
            x_coords = time_frames
            y_coords = np.arange(len(band_names))
            X, Y = np.meshgrid(x_coords, y_coords)
            Z = landscape
            
            # Crear superficie estructurada
            mesh = pv.StructuredGrid(X, Y, Z)
            mesh['intensity'] = Z.ravel()
            
            # Agregar superficie al plotter con colores vibrantes
            self.plotter.add_mesh(
                mesh,
                scalars='intensity',
                cmap='plasma',
                opacity=0.9,
                smooth_shading=True,
                show_scalar_bar=True,
                scalar_bar_args={'title': '🔊 Intensidad', 'color': 'white'}
            )
            
            # Configurar ejes con etiquetas descriptivas
            self.plotter.add_text(
                "🕐 TIEMPO (segundos)",
                position='lower_left',
                font_size=14,
                color='cyan'
            )
            
            self.plotter.add_text(
                f"🎵 BANDAS: {', '.join(band_names).upper()}",
                position='lower_right',
                font_size=12,
                color='orange'
            )
            
            self.plotter.add_text(
                f"🏔️ Paisaje Sonoro 3D\n📊 {landscape.shape[1]} frames × {landscape.shape[0]} bandas",
                position='upper_left',
                font_size=12,
                color='white'
            )
            
            # Configurar cámara para vista óptima
            self.plotter.camera_position = 'iso'
            self.plotter.camera.azimuth = 45
            self.plotter.camera.elevation = 30
            
            # Configurar iluminación
            self.plotter.enable_shadows()
            
            # Mostrar ventana 3D
            self.plotter.show(interactive_update=True)
            
            self.results_text.insert(tk.END, "🚀 Ventana 3D abierta!\n")
            self.results_text.insert(tk.END, "   • Mouse: Rotar vista\n")
            self.results_text.insert(tk.END, "   • Scroll: Zoom\n")
            self.results_text.insert(tk.END, "   • Click derecho: Pan\n")
            
        except Exception as e:
            messagebox.showerror("Error 3D", f"Error abriendo visualización:\n{str(e)}")
            
    def export_html(self):
        """Exportar HTML interactivo"""
        if not self.journey_data:
            messagebox.showerror("Error", "No hay datos para exportar")
            return
            
        try:
            # Pedir ubicación de guardado
            file_path = filedialog.asksaveasfilename(
                title="Guardar datos de análisis",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                # Exportar resumen del análisis
                import json
                
                # Crear resumen exportable
                export_data = {
                    'filename': os.path.basename(self.current_file),
                    'duration': self.journey_data['duration'],
                    'journey_stats': self.journey_data['journey_stats'],
                    'freq_bands_info': {
                        band: {
                            'shape': self.journey_data['freq_bands'][band]['magnitude'].shape,
                            'time_frames': len(self.journey_data['freq_bands'][band]['times'])
                        } for band in self.journey_data['freq_bands'].keys()
                    }
                }
                
                if file_path.endswith('.json'):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(export_data, f, indent=2, ensure_ascii=False)
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("🎵 SOUNDGRAPH DESKTOP - Análisis de Audio\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(f"📄 Archivo: {export_data['filename']}\n")
                        f.write(f"⏱️ Duración: {export_data['duration']:.2f} segundos\n")
                        f.write(f"📊 Frames: {export_data['journey_stats']['total_frames']}\n")
                        f.write(f"🎵 Bandas: {export_data['journey_stats']['freq_bands']}\n")
                        f.write(f"🔍 Puntos: {export_data['journey_stats']['mesh_points']}\n\n")
                        
                        f.write("🔊 Análisis por Banda de Frecuencia:\n")
                        f.write("-" * 30 + "\n")
                        for band, info in export_data['freq_bands_info'].items():
                            f.write(f"{band.upper()}: {info['shape'][0]} freq × {info['time_frames']} frames\n")
                
                self.results_text.insert(tk.END, f"💾 Datos exportados: {os.path.basename(file_path)}\n")
                messagebox.showinfo("Exportación", "Datos guardados exitosamente!")
                    
        except Exception as e:
            messagebox.showerror("Error Exportación", f"Error guardando datos:\n{str(e)}")
            
    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()

def main():
    """Función principal"""
    print("🎵 Iniciando SoundGraph Desktop...")
    
    try:
        app = SoundGraphDesktop()
        app.run()
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")

if __name__ == "__main__":
    main() 