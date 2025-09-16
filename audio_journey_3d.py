"""
🎵 AUDIO JOURNEY 3D ENGINE 🏔️
===========================
Visualización 3D avanzada con PyVista para un "viaje completo" por una canción
- Separación de graves, medios y agudos
- Navegación temporal completa (1 minuto+)
- Exportación HTML interactiva
- Sincronización con reproducción de audio
"""

import librosa
import numpy as np
import pyvista as pv
from scipy.ndimage import gaussian_filter, zoom
from scipy.signal import butter, filtfilt
from sklearn.preprocessing import StandardScaler
import io
import base64

class AudioJourney3D:
    def __init__(self):
        """Inicializar el motor de visualización 3D"""
        self.sr = 22050  # Sample rate optimizado
        self.hop_length = 512
        self.n_fft = 2048
        
        # Configuración de bandas de frecuencia
        self.freq_bands = {
            'bass': (20, 250),      # Graves
            'mids': (250, 4000),    # Medios  
            'highs': (4000, 11025)  # Agudos
        }
        
        # Configuración 3D
        self.mesh_resolution = (80, 200)  # (freq_bands, time_frames)
        
    def process_full_journey(self, audio_file_path, duration_minutes=1.0):
        """
        Procesar audio completo para generar viaje 3D
        """
        try:
            print(f"🎵 Cargando audio para viaje de {duration_minutes} minutos...")
            
            # Cargar audio completo (hasta duration_minutes)
            max_duration = duration_minutes * 60  # Convertir a segundos
            y, sr = librosa.load(audio_file_path, sr=self.sr, duration=max_duration)
            
            print(f"✅ Audio cargado: {len(y)/sr:.2f} segundos")
            
            # 1. SEPARAR BANDAS DE FRECUENCIA
            print("🔊 Separando graves, medios y agudos...")
            freq_bands_data = self._separate_frequency_bands(y, sr)
            
            # 2. GENERAR ESPECTROGRAMA 3D TEMPORAL
            print("🏔️ Generando paisaje 3D temporal...")
            journey_3d_data = self._create_temporal_landscape(freq_bands_data, sr)
            
            # 3. CREAR MESH 3D CON PYVISTA
            print("✨ Creando mesh 3D interactivo...")
            html_content = self._create_pyvista_journey(journey_3d_data)
            
            # 4. DATOS PARA SINCRONIZACIÓN
            sync_data = self._create_sync_data(y, sr, journey_3d_data)
            
            return {
                'success': True,
                'duration': len(y) / sr,
                'pyvista_data': html_content,  # Ahora contiene datos estructurados
                'sync_data': sync_data,
                'freq_bands': freq_bands_data,
                'journey_stats': {
                    'total_frames': journey_3d_data['time_frames'].shape[0],
                    'freq_bands': len(self.freq_bands),
                    'mesh_points': journey_3d_data['landscape'].size
                }
            }
            
        except Exception as e:
            print(f"❌ Error en journey 3D: {e}")
            return {'success': False, 'error': str(e)}
    
    def _separate_frequency_bands(self, y, sr):
        """Separar audio en graves, medios y agudos usando filtros"""
        bands_data = {}
        
        for band_name, (low_freq, high_freq) in self.freq_bands.items():
            # Diseñar filtro Butterworth
            nyquist = sr / 2
            low = max(low_freq / nyquist, 0.01)  # Evitar frecuencias muy bajas
            high = min(high_freq / nyquist, 0.99)  # Evitar frecuencias muy altas
            
            # Verificar que las frecuencias sean válidas
            if low >= high:
                print(f"⚠️ Saltando banda {band_name}: frecuencias inválidas")
                continue
                
            # Filtro pasa banda
            b, a = butter(4, [low, high], btype='band')
            filtered_audio = filtfilt(b, a, y)
            
            # Generar espectrograma para esta banda
            stft = librosa.stft(filtered_audio, 
                              hop_length=self.hop_length,
                              n_fft=self.n_fft)
            magnitude = np.abs(stft)
            
            # Convertir a dB y normalizar
            magnitude_db = librosa.amplitude_to_db(magnitude, ref=np.max)
            normalized = (magnitude_db - magnitude_db.min()) / (magnitude_db.max() - magnitude_db.min())
            
            bands_data[band_name] = {
                'magnitude': normalized,
                'frequencies': librosa.fft_frequencies(sr=sr, n_fft=self.n_fft),
                'times': librosa.frames_to_time(np.arange(magnitude.shape[1]), 
                                              sr=sr, hop_length=self.hop_length)
            }
            
            print(f"  ✅ {band_name.upper()}: {low_freq}-{high_freq}Hz procesado")
        
        return bands_data
    
    def _create_temporal_landscape(self, freq_bands_data, sr):
        """Crear paisaje 3D que representa toda la canción"""
        
        # Obtener dimensiones temporales comunes
        min_time_frames = min(data['magnitude'].shape[1] for data in freq_bands_data.values())
        time_frames = librosa.frames_to_time(np.arange(min_time_frames), 
                                           sr=sr, hop_length=self.hop_length)
        
        # Crear matriz 3D: [bandas_freq, tiempo, elevación]
        # Cada banda de frecuencia se convierte en una "capa" del paisaje
        landscape_layers = []
        band_names = []
        
        for band_name, band_data in freq_bands_data.items():
            # Truncar a min_time_frames
            magnitude = band_data['magnitude'][:, :min_time_frames]
            
            # Interpolar para crear resolución uniforme
            # Resumir frecuencias en cada banda (promedio de intensidad)
            band_intensity = np.mean(magnitude, axis=0)  # Promedio por frame temporal
            
            landscape_layers.append(band_intensity)
            band_names.append(band_name)
        
        # Crear paisaje 3D apilado
        landscape = np.array(landscape_layers)  # Shape: (3, time_frames)
        
        # Suavizar el paisaje temporalmente
        landscape_smooth = gaussian_filter(landscape, sigma=[0.5, 2.0])
        
        # Crear coordenadas 3D
        # X = Tiempo, Y = Banda de frecuencia, Z = Intensidad
        time_coords = time_frames
        band_coords = np.arange(len(band_names))  # 0=bass, 1=mids, 2=highs
        
        return {
            'landscape': landscape_smooth,
            'time_frames': time_coords,
            'freq_bands': band_coords,
            'band_names': band_names,
            'shape': landscape_smooth.shape
        }
    
    def _create_pyvista_journey(self, journey_data):
        """Crear datos de visualización 3D para PyVista (sin renderizar)"""
        
        landscape = journey_data['landscape']
        time_frames = journey_data['time_frames']
        band_names = journey_data['band_names']
        
        # En lugar de crear HTML, retornamos los datos estructurados
        # para que la aplicación desktop los use directamente
        
        return {
            'landscape': landscape,
            'time_frames': time_frames,
            'band_names': band_names,
            'shape': landscape.shape,
            'status': 'ready_for_desktop'
        }
    
    def _create_sync_data(self, y, sr, journey_data):
        """Crear datos para sincronización temporal con audio"""
        
        # Generar markers temporales cada segundo
        duration = len(y) / sr
        time_markers = np.arange(0, duration, 1.0)  # Cada segundo
        
        # Para cada marker, encontrar la posición en el landscape
        landscape_positions = []
        
        for marker_time in time_markers:
            # Encontrar frame más cercano
            frame_idx = int(marker_time * sr / self.hop_length)
            if frame_idx < journey_data['landscape'].shape[1]:
                # Obtener intensidades de las 3 bandas en este momento
                bass_intensity = journey_data['landscape'][0, frame_idx]
                mids_intensity = journey_data['landscape'][1, frame_idx]
                highs_intensity = journey_data['landscape'][2, frame_idx]
                
                landscape_positions.append({
                    'time': marker_time,
                    'bass': float(bass_intensity),
                    'mids': float(mids_intensity), 
                    'highs': float(highs_intensity),
                    'frame_idx': frame_idx
                })
        
        return {
            'markers': landscape_positions,
            'duration': duration,
            'total_frames': journey_data['landscape'].shape[1],
            'fps': sr / self.hop_length  # Frames por segundo
        }

# Función helper para integración con FastAPI
def generate_audio_journey_3d(audio_file_path, duration_minutes=1.0):
    """Función principal para generar viaje 3D"""
    engine = AudioJourney3D()
    return engine.process_full_journey(audio_file_path, duration_minutes) 