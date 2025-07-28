import librosa
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import io
import base64
from scipy import signal
import json
from pydub import AudioSegment
import tempfile
import os

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 22050  # Sample rate estándar para análisis
        
    async def process_audio(self, file_path: str, filename: str):
        """Procesar archivo de audio y generar todas las visualizaciones"""
        try:
            # Convertir MP3 a WAV temporalmente si es necesario
            processed_path = file_path
            if filename.lower().endswith('.mp3'):
                processed_path = self._convert_mp3_to_wav(file_path)
            
            # Cargar audio
            y, sr = librosa.load(processed_path, sr=self.sample_rate)
            duration = len(y) / sr
            
            # Limpiar archivo temporal si se creó
            if processed_path != file_path and os.path.exists(processed_path):
                os.unlink(processed_path)
            
            # Calcular BPM
            bpm = self.calculate_bpm(y, sr)
            
            # Generar visualizaciones
            waveform_data = self.generate_colorful_waveform(y, sr)
            mel_spectrogram_img = self.generate_mel_spectrogram_image(y, sr)
            mel_spectrogram_3d = self.generate_mel_spectrogram_3d(y, sr)
            frequency_analyzer = self.generate_frequency_analyzer(y, sr)
            
            return {
                "filename": filename,
                "duration": round(duration, 2),
                "bpm": round(bpm, 1),
                "sample_rate": sr,
                "waveform": waveform_data,
                "mel_spectrogram": mel_spectrogram_img,
                "mel_spectrogram_3d": mel_spectrogram_3d,
                "frequency_analyzer": frequency_analyzer,
                "success": True
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def calculate_bpm(self, y, sr):
        """Calcular BPM automáticamente"""
        try:
            # Usar librosa para detectar tempo
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            return float(tempo)
        except:
            return 120.0  # BPM por defecto si falla la detección
    
    def generate_colorful_waveform(self, y, sr):
        """Generar waveform realista con múltiples bandas de frecuencia"""
        try:
            # Parámetros para mayor resolución
            hop_length = 256  # Más resolución temporal
            n_fft = 2048
            
            # Calcular STFT
            D = librosa.stft(y, hop_length=hop_length, n_fft=n_fft)
            magnitude = np.abs(D)
            
            # Crear bandas de frecuencia más realistas (como un espectro visual)
            freq_bins = np.fft.rfftfreq(n_fft, 1/sr)
            
            # Definir 10 bandas de frecuencia con rangos realistas
            frequency_bands = [
                (20, 50),      # Sub-Bass profundo
                (50, 100),     # Bass bajo
                (100, 200),    # Bass medio
                (200, 400),    # Low-Mid
                (400, 800),    # Mid-Low
                (800, 1600),   # Mid
                (1600, 3200),  # Mid-High  
                (3200, 6400),  # High-Mid
                (6400, 12800), # Treble
                (12800, 20000) # Brilliance/Air
            ]
            
            # Colores que simulan el espectro visual de frecuencias
            # De graves (rojos) a agudos (violetas), como un arcoíris de audio
            band_colors = [
                '#8B0000',  # Sub-Bass - Rojo muy oscuro
                '#DC143C',  # Bass bajo - Rojo carmesí
                '#FF4500',  # Bass medio - Naranja rojizo
                '#FF8C00',  # Low-Mid - Naranja oscuro
                '#FFD700',  # Mid-Low - Dorado
                '#ADFF2F',  # Mid - Verde lima
                '#00FF7F',  # Mid-High - Verde primavera  
                '#00CED1',  # High-Mid - Turquesa
                '#4169E1',  # Treble - Azul royal
                '#8A2BE2'   # Air - Azul violeta
            ]
            
            band_names = [
                'Sub-Bass', 'Bass-Bajo', 'Bass-Medio', 'Low-Mid', 'Mid-Low', 
                'Mid', 'Mid-High', 'High-Mid', 'Treble', 'Air'
            ]
            
            # Calcular energía por cada banda
            time_frames = librosa.frames_to_time(np.arange(magnitude.shape[1]), sr=sr, hop_length=hop_length)
            
            band_energies = []
            band_data = {}
            
            for i, (low_f, high_f) in enumerate(frequency_bands):
                # Encontrar índices de frecuencia para esta banda
                band_mask = (freq_bins >= low_f) & (freq_bins <= high_f)
                
                if np.sum(band_mask) > 0:
                    # Calcular energía promedio en esta banda
                    band_energy = np.mean(magnitude[band_mask], axis=0)
                    
                    # Normalizar individualmente cada banda
                    if np.max(band_energy) > 0:
                        band_energy = band_energy / np.max(band_energy)
                else:
                    band_energy = np.zeros(magnitude.shape[1])
                
                band_energies.append(band_energy.tolist())
                
                # Guardar datos para el frontend
                band_data[f'band_{i}'] = {
                    'name': band_names[i],
                    'color': band_colors[i],
                    'energy': band_energy.tolist(),
                    'freq_range': f'{low_f}-{high_f}Hz'
                }
            
            return {
                "time": time_frames.tolist(),
                "bands": band_data,
                "band_count": len(frequency_bands)
            }
            
        except Exception as e:
            print(f"Error en waveform: {e}")
            return {"error": str(e)}
    
    def generate_mel_spectrogram_image(self, y, sr):
        """Generar imagen mel-spectrogram estilo IA generativa con alta resolución"""
        try:
            # Crear mel-spectrogram con MÁS resolución
            mel_spec = librosa.feature.melspectrogram(
                y=y, sr=sr, 
                n_mels=256,  # Más bandas mel (era 128)
                fmax=sr//2,  # Rango completo de frecuencias
                hop_length=256,  # Más resolución temporal (era 512)
                n_fft=2048   # Más resolución frecuencial
            )
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Crear figura MÁS GRANDE y bonita
            fig, ax = plt.subplots(figsize=(16, 8))
            img = librosa.display.specshow(
                mel_spec_db, 
                y_axis='mel', 
                x_axis='time', 
                sr=sr, 
                fmax=sr//2, 
                ax=ax, 
                cmap='plasma',  # Colormap más bonito que viridis
                shading='gouraud'  # Suavizado
            )
            
            ax.set_title('🤖 Representación IA Generativa (Mel-Spectrogram HD)', fontsize=16, color='white')
            ax.set_xlabel('Tiempo (s)', fontsize=12, color='white')
            ax.set_ylabel('Frecuencia Mel (Hz)', fontsize=12, color='white')
            
            # Fondo negro para que se vea como software profesional
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')
            ax.tick_params(colors='white')
            
            # Colorbar mejorado
            cbar = fig.colorbar(img, ax=ax, format='%+2.0f dB')
            cbar.ax.yaxis.label.set_color('white')
            cbar.ax.tick_params(colors='white')
            
            # Convertir a base64 con MAYOR resolución
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                       facecolor='black', edgecolor='none')
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            print(f"Error en mel-spectrogram: {e}")
            return None
    
    def generate_frequency_analyzer(self, y, sr):
        """Generar analizador de espectro por frames - 'fotos de cada segundo'"""
        try:
            # Dividir audio en frames de ~1 segundo
            frame_length = sr  # 1 segundo de audio
            hop_length = sr // 2  # Overlap de 50%
            
            # Calcular STFT para cada frame
            D = librosa.stft(y, hop_length=hop_length, n_fft=2048)
            magnitude = np.abs(D)
            
            # Convertir a dB
            magnitude_db = librosa.amplitude_to_db(magnitude, ref=np.max)
            
            # Crear bandas de frecuencia como un EQ (estilo plugin de audio)
            freq_bins = np.fft.rfftfreq(2048, 1/sr)
            
            # Definir 8 bandas como un EQ profesional
            bands = [
                (20, 60),      # Sub-Bass
                (60, 200),     # Bass  
                (200, 500),    # Low-Mid
                (500, 1000),   # Mid
                (1000, 2000),  # Upper-Mid
                (2000, 4000),  # Presence
                (4000, 8000),  # Brilliance
                (8000, 20000)  # Air
            ]
            
            band_names = ['Sub-Bass', 'Bass', 'Low-Mid', 'Mid', 'Upper-Mid', 'Presence', 'Brilliance', 'Air']
            
            # Calcular energía por banda y por frame temporal
            time_frames = librosa.frames_to_time(np.arange(magnitude.shape[1]), sr=sr, hop_length=hop_length)
            
            band_energies = []
            for low_f, high_f in bands:
                # Encontrar bins de frecuencia para esta banda
                band_mask = (freq_bins >= low_f) & (freq_bins <= high_f)
                if np.sum(band_mask) > 0:
                    # Promediar energía en esta banda por cada frame temporal
                    band_energy = np.mean(magnitude_db[band_mask], axis=0)
                else:
                    band_energy = np.zeros(magnitude.shape[1])
                band_energies.append(band_energy.tolist())
            
            return {
                "time_frames": time_frames.tolist(),
                "band_names": band_names,
                "band_energies": band_energies,
                "frame_duration": hop_length / sr  # Duración de cada frame
            }
            
        except Exception as e:
            print(f"Error en analizador de frecuencias: {e}")
            return {"error": str(e)}
    
    def _convert_mp3_to_wav(self, mp3_path: str):
        """Convertir MP3 a WAV usando pydub para mejor compatibilidad"""
        try:
            print(f"Convirtiendo MP3 a WAV: {mp3_path}")
            
            # Cargar MP3 con pydub
            audio = AudioSegment.from_mp3(mp3_path)
            
            # Crear archivo temporal WAV
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                wav_path = tmp.name
            
            # Exportar como WAV
            audio.export(wav_path, format='wav')
            
            print(f"Conversión exitosa: {wav_path}")
            return wav_path
            
        except Exception as e:
            print(f"Error convirtiendo MP3: {e}")
            return mp3_path  # Devolver el original y que librosa lo intente
    
    def generate_mel_spectrogram_3d(self, y, sr):
        """Generar mel-spectrogram 3D con INTERPOLACIÓN SUAVE y alta resolución"""
        try:
            # Crear mel-spectrogram de ALTA RESOLUCIÓN
            mel_spec = librosa.feature.melspectrogram(
                y=y, sr=sr,
                n_mels=50,          # Más bandas para mejor resolución
                fmax=sr//2,         # Frecuencia máxima = Nyquist
                hop_length=512,     # Más resolución temporal
                n_fft=2048,
                window='hann'       # Ventana Hann para suavizado
            )
            
            # Convertir a dB y normalizar
            mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
            mel_spec_normalized = (mel_spec_db - np.min(mel_spec_db)) / (np.max(mel_spec_db) - np.min(mel_spec_db))
            
            # INTERPOLACIÓN CON UPSAMPLING - Crear superficie más suave
            from scipy.ndimage import gaussian_filter, zoom
            
            # 1. Suavizar con filtro gaussiano 
            mel_spec_smooth = gaussian_filter(mel_spec_normalized, sigma=1.2)
            
            # 2. UPSAMPLING para interpolación - Crear más puntos
            zoom_factors = (1.5, 1.5)  # 1.5x más puntos en ambas dimensiones
            mel_spec_interp = zoom(mel_spec_smooth, zoom_factors, order=3, mode='reflect')
            
            # Crear ejes con INTERPOLACIÓN
            original_time_frames = librosa.frames_to_time(np.arange(mel_spec.shape[1]), sr=sr, hop_length=512)
            original_mel_frequencies = librosa.mel_frequencies(n_mels=50, fmax=sr//2)
            
            # EJES INTERPOLADOS con más puntos
            time_frames = np.linspace(0, original_time_frames[-1], mel_spec_interp.shape[1])
            mel_frequencies = np.linspace(original_mel_frequencies[0], original_mel_frequencies[-1], mel_spec_interp.shape[0])
            
            # FORMATO SURFACE INTERPOLADO
            return {
                "z_matrix": mel_spec_interp.tolist(),                    # Matriz Z interpolada
                "x_axis": [float(t) for t in time_frames],               # Eje X (tiempo interpolado) 
                "y_axis": [float(f) for f in mel_frequencies],           # Eje Y (frecuencias interpoladas)
                "duration": float(time_frames[-1]) if len(time_frames) > 0 else 0.0,
                "max_freq": float(sr//2),
                "min_freq": float(mel_frequencies[0]),
                "shape": mel_spec_interp.shape,
                "interpolated": True                                     # Flag de interpolación
            }
            
        except Exception as e:
            print(f"Error en mel-spectrogram 3D: {e}")
            return {"error": str(e)} 