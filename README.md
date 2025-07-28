# 🎵 SoundGraph DJ

**Análisis visual profesional de audio para DJs**

Una aplicación web minimalista que permite analizar archivos de audio y generar visualizaciones profesionales como las que encuentras en Serato, Virtual DJ, Traktor y Ableton Live.

## ✨ Características

### 🎨 Visualizaciones Incluidas
1. **Waveform Colorido** - Estilo Serato/VirtualDJ con separación por frecuencias (Graves=Rojo, Medios=Verde, Agudos=Azul)
2. **Representación IA Generativa** - Mel-Spectrogram como imagen (estilo Riffusion/Stable Audio)
3. **Espectrograma Ableton** - Frecuencias vs tiempo con colores dinámicos

### 🔧 Funcionalidades
- ⚡ **Cálculo automático de BPM**
- 🎧 **Soporte múltiples formatos**: MP3, WAV, M4A, FLAC
- 📱 **Drag & Drop** minimalista
- 🎯 **API REST** con FastAPI
- 🌈 **Interfaz moderna** con gradientes y animaciones

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8+
- pip

### 1. Clonar e instalar dependencias
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python main.py
```

### 2. Abrir en navegador
```
http://localhost:8000
```

## 📖 Uso

1. **Arrastra** tu archivo de audio a la zona de drop
2. **Espera** el análisis (unos segundos)
3. **Disfruta** las 3 visualizaciones generadas automáticamente
4. El **BPM** se calcula automáticamente

## 🛠️ Stack Técnico

### Backend (Python)
- **FastAPI** - API REST ultrarrápida
- **Librosa** - Análisis de audio profesional  
- **Matplotlib** - Gráficos estáticos
- **Plotly** - Visualizaciones interactivas
- **NumPy + SciPy** - Procesamiento matemático

### Frontend
- **HTML5 + CSS3** - Minimalista y moderno
- **JavaScript ES6** - Sin frameworks pesados
- **Plotly.js** - Gráficos interactivos
- **Drag & Drop API** - UX fluida

## 📁 Estructura del Proyecto

```
soundgraph/
├── main.py                 # Servidor FastAPI
├── audio_processor.py      # Procesamiento de audio
├── requirements.txt        # Dependencias Python
├── templates/
│   └── index.html         # Frontend principal
└── static/
    ├── style.css          # Estilos CSS
    └── script.js          # JavaScript frontend
```

## 🎯 Próximas Características

- 🤖 **Machine Learning**: Comparación de similitudes entre canciones
- 🥁 **Beat Detection**: Detección automática de golpes/drums
- 📊 **Análisis Científico**: Métricas avanzadas de cada canción
- 🔄 **Comparador**: Overlay de múltiples tracks
- 💾 **Exportar**: Guardar análisis en formato JSON/CSV

## 🎛️ Para DJs

Esta herramienta es perfecta para:
- **Análisis de sets**: Entender la estructura de tus tracks
- **Preparación**: Conocer BPM y características antes del set
- **Educación**: Aprender cómo se ve cada tipo de música
- **Creatividad**: Inspirarse con las visualizaciones para nuevos sets

## 🐛 Troubleshooting

### Error de instalación de librosa
```bash
# En Mac con M1/M2
pip install librosa --no-deps
pip install numba llvmlite

# En Linux
sudo apt-get install libsndfile1
```

### Puerto ocupado
```bash
# Cambiar puerto en main.py línea final:
uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
```

## 📝 Licencia

MIT License - Úsalo como quieras 🚀

---

**¡Hecho con ❤️ por un DJ que programa!** 🎧💻 