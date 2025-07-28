# 🎵 SoundGraph Desktop - Aplicación Nativa 3D

**Explora tu música en 3D con PyVista - Separación de Graves, Medios y Agudos**

## 🚀 ¿Qué es SoundGraph Desktop?

Una aplicación **nativa de escritorio** que analiza archivos de audio y genera **visualizaciones 3D interactivas** del paisaje sonoro, separando automáticamente:

- 🎵 **GRAVES** (20-250 Hz)
- 🎶 **MEDIOS** (250-4000 Hz) 
- 🎵 **AGUDOS** (4000-11025 Hz)

## ✨ Características

### 🏔️ **Visualización 3D Nativa**
- **PyVista** para renderizado científico de alta calidad
- **Navegación fluida** con mouse (rotar, zoom, pan)
- **Iluminación avanzada** y sombras
- **Colores vibrantes** con colormap plasma

### 🔬 **Análisis Científico**
- **Filtros Butterworth** de 4º orden
- **Separación precisa** de bandas de frecuencia
- **Suavizado gaussiano** para superficies continuas
- **Interpolación cúbica** para resolución HD

### 🖥️ **Interfaz Intuitiva**
- **Interfaz gráfica moderna** con tkinter
- **Drag & drop** de archivos
- **Análisis en tiempo real** con barra de progreso
- **Exportación de datos** en TXT/JSON

## 🛠️ Instalación

### 1. **Activar entorno virtual**
```bash
source venv/bin/activate
```

### 2. **Verificar instalación**
```bash
python -c "import pyvista; print('✅ PyVista OK')"
```

### 3. **Ejecutar aplicación**
```bash
python soundgraph_desktop.py
```

**O usa el launcher:**
```bash
python run_desktop.py
```

## 🎯 Cómo usar

### **Paso 1: Seleccionar Audio**
1. Click en **"🎧 Seleccionar Audio"**
2. Elige tu archivo (**WAV recomendado**, MP3 también funciona)
3. Ajusta la **duración** a analizar (0.5 - 5.0 minutos)

### **Paso 2: Generar Análisis**
1. Click en **"🚀 Generar Viaje 3D"**
2. Espera el análisis (puede tardar 30-60 segundos)
3. Revisa los **resultados** en el área de texto

### **Paso 3: Explorar en 3D**
1. Click en **"🏔️ Abrir Visualización 3D"**
2. **Se abre una ventana 3D separada**
3. Usa el mouse para navegar:
   - **Arrastrar**: Rotar vista
   - **Scroll**: Zoom in/out
   - **Click derecho + arrastrar**: Pan

### **Paso 4: Exportar (Opcional)**
1. Click en **"💾 Exportar Datos"**
2. Guarda análisis en **TXT** o **JSON**

## 🎵 Formatos Soportados

| Formato | Estado | Notas |
|---------|--------|-------|
| **WAV** | ✅ Perfecto | Recomendado para mejor calidad |
| **MP3** | ⚠️ Funciona | Requiere ffmpeg instalado |
| **M4A** | ⚠️ Funciona | Requiere ffmpeg instalado |
| **FLAC** | ✅ Perfecto | Alta calidad |

## 🔧 Solución de Problemas

### **Error: "No module named 'pyvista'"**
```bash
source venv/bin/activate
pip install "pyvista>=0.43.0"
```

### **Error con MP3: "ffmpeg not found"**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### **La ventana 3D no se abre**
- Verifica que tu sistema tenga **soporte gráfico**
- En macOS: asegúrate que **XQuartz** esté instalado
- En Linux: verifica que **X11** esté funcionando

### **Aplicación se congela**
- Usa archivos de **duración corta** (1-2 minutos máximo)
- Prueba con **formato WAV** en lugar de MP3
- Reinicia la aplicación

## 💡 Consejos de Uso

### **Para mejores resultados:**
1. **Usa archivos WAV** de alta calidad
2. **Analiza 1-2 minutos** para empezar
3. **Elige música con variedad** (graves y agudos)
4. **Cierra otras aplicaciones** pesadas durante el análisis

### **Navegación 3D:**
- **Comienza con zoom out** para ver toda la superficie
- **Busca "montañas"** - representan partes intensas
- **Compara diferentes bandas** de frecuencia
- **Rota lentamente** para apreciar el paisaje completo

## 🌊 Interpretación del Paisaje 3D

### **Ejes:**
- **X (horizontal)**: Tiempo en segundos
- **Y (profundidad)**: Bandas de frecuencia (Graves → Medios → Agudos)
- **Z (altura)**: Intensidad sonora

### **Colores:**
- **Púrpura/Negro**: Silencio o intensidad baja
- **Azul/Cyan**: Intensidad media
- **Amarillo/Naranja**: Intensidad alta
- **Rosa/Blanco**: Intensidad máxima

### **Formas:**
- **Valles**: Momentos silenciosos
- **Colinas**: Variaciones suaves
- **Montañas**: Picos de intensidad (beats, crashes)
- **Mesetas**: Sonidos sostenidos

## 🚀 Próximas Funcionalidades

- [ ] **Reproducción sincronizada** con marcador 3D
- [ ] **Múltiples archivos** para comparación
- [ ] **Detección de beats** automática
- [ ] **Exportación a STL** para impresión 3D
- [ ] **Análisis de tempo** y ritmo
- [ ] **Filtros personalizados** de frecuencia

## 📊 Especificaciones Técnicas

| Componente | Detalles |
|------------|----------|
| **Motor 3D** | PyVista + VTK 9.4.2 |
| **Análisis Audio** | Librosa + SciPy |
| **Filtros** | Butterworth 4º orden |
| **Resolución** | 50 mels × 512 hop_length |
| **Interpolación** | Cúbica con zoom 1.5x |
| **Suavizado** | Gaussiano σ=1.2 |

---

**🎵 ¡Disfruta explorando tu música en 3D!** 🏔️ 