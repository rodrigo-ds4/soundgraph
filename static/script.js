// Variables globales
let currentAudioData = null;
let audioPlayer = null;
let currentAudioBlob = null;
let plot3DRef = null;

// Elementos del DOM
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const trackInfo = document.getElementById('trackInfo');
const loadingSpinner = document.getElementById('loadingSpinner');
const visualizations = document.getElementById('visualizations');
const errorMessage = document.getElementById('errorMessage');

// Inicializar eventos
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Drag & Drop
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);
    dropZone.addEventListener('click', () => fileInput.click());
    
    // File input
    fileInput.addEventListener('change', handleFileSelect);
    selectBtn.addEventListener('click', () => fileInput.click());
}

// Drag & Drop handlers
function handleDragOver(e) {
    e.preventDefault();
    dropZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
}

// Procesar archivo
async function processFile(file) {
    // Validar formato
    const validFormats = ['mp3', 'wav', 'm4a', 'flac'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (!validFormats.includes(fileExtension)) {
        showError('Formato no soportado. Usa MP3, WAV, M4A o FLAC');
        return;
    }
    
    // Mostrar loading
    showLoading(true);
    hideError();
    
    try {
        // Crear FormData
        const formData = new FormData();
        formData.append('file', file);
        
        // Guardar el archivo para el reproductor
        currentAudioBlob = file;
        
        // Enviar a backend
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentAudioData = result;
            displayResults(result);
        } else {
            showError(result.error || 'Error procesando el archivo');
        }
        
    } catch (error) {
        showError(`Error de conexión: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// Mostrar resultados
function displayResults(data) {
    // Mostrar info del track
    document.getElementById('fileName').textContent = data.filename;
    document.getElementById('duration').textContent = `${data.duration}s`;
    document.getElementById('bpm').textContent = `${data.bpm} BPM`;
    
    trackInfo.classList.remove('hidden');
    visualizations.classList.remove('hidden');
    
    // Generar visualizaciones
    createColorfulWaveform(data.waveform);
    createMelSpectrogram(data.mel_spectrogram);
    createMelSpectrogram3DPreviewWithOptions(data.mel_spectrogram_3d, 'surface', 'viridis');
    
    // Configurar reproductor de audio
    setupAudioPlayer();
    
    // Configurar botones fullscreen
    setupFullscreenButtons(data.mel_spectrogram_3d);
}

// 1. Waveform Realista con Múltiples Bandas
function createColorfulWaveform(waveformData) {
    if (!waveformData || waveformData.error) {
        console.error('Error en waveform data:', waveformData);
        return;
    }
    
    // Crear traces para cada banda de frecuencia
    const traces = [];
    
    // Iterar sobre todas las bandas
    for (let i = 0; i < waveformData.band_count; i++) {
        const bandKey = `band_${i}`;
        const bandInfo = waveformData.bands[bandKey];
        
        if (bandInfo) {
            // Convertir color hex a rgba para transparencia
            const hexColor = bandInfo.color;
            const rgbaColor = hexToRgba(hexColor, 0.7);
            
            traces.push({
                x: waveformData.time,
                y: bandInfo.energy,
                name: `${bandInfo.name} (${bandInfo.freq_range})`,
                type: 'scatter',
                mode: 'lines',
                fill: 'tonexty',
                line: { 
                    color: hexColor, 
                    width: 1.5 
                },
                fillcolor: rgbaColor,
                hovertemplate: `<b>${bandInfo.name}</b><br>` +
                              `Frecuencia: ${bandInfo.freq_range}<br>` +
                              `Tiempo: %{x:.2f}s<br>` +
                              `Energía: %{y:.3f}<br>` +
                              `<extra></extra>`
            });
        }
    }
    
    const layout = {
        title: {
            text: '🌈 Waveform Realista - Espectro de Frecuencias',
            font: { color: '#ffffff', size: 16 }
        },
        xaxis: {
            title: 'Tiempo (segundos)',
            color: '#ffffff',
            gridcolor: 'rgba(255, 255, 255, 0.2)'
        },
        yaxis: {
            title: 'Energía Normalizada',
            color: '#ffffff',
            gridcolor: 'rgba(255, 255, 255, 0.2)'
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0.3)',
        font: { color: '#ffffff' },
        legend: {
            font: { color: '#ffffff', size: 9 },
            orientation: 'v',
            x: 1.02,
            y: 1,
            bgcolor: 'rgba(0,0,0,0.5)',
            bordercolor: 'rgba(255,255,255,0.2)',
            borderwidth: 1
        },
        showlegend: true,
        hovermode: 'closest'
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d']
    };
    
    Plotly.newPlot('colorfulWaveform', traces, layout, config);
}

// Función auxiliar para convertir hex a rgba
function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// 2. Mel-Spectrogram
function createMelSpectrogram(melSpectrogramData) {
    const container = document.getElementById('melSpectrogramImg');
    
    if (melSpectrogramData) {
        container.src = melSpectrogramData;
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
        console.error('No mel-spectrogram data available');
    }
}

// 3. Mel-Spectrogram 3D Topográfico OPTIMIZADO
function createMelSpectrogram3D(mel3DData) {
    if (!mel3DData || mel3DData.error) {
        console.error('Error en mel 3D data:', mel3DData);
        return;
    }
    
    // SURFACE 3D INTERPOLADO - Superficie suave y continua
    const trace = {
        z: mel3DData.z_matrix,
        x: mel3DData.x_axis,
        y: mel3DData.y_axis,
        type: 'surface',
        
        // INTERPOLACIÓN ACTIVADA - Para superficie continua
        hidesurface: false,
        connectgaps: true,
        
        // COLORSCALE optimizada para mesh3d
        colorscale: [
            [0.0, '#000428'],     // Azul noche profunda
            [0.1, '#004e92'],     // Azul océano profundo  
            [0.2, '#009ffd'],     // Azul cielo
            [0.3, '#00d2ff'],     // Cyan brillante
            [0.4, '#7209b7'],     // Púrpura vibrante
            [0.5, '#a663cc'],     // Magenta suave
            [0.6, '#d1004e'],     // Rosa intenso  
            [0.7, '#ff6b35'],     // Naranja volcánico
            [0.8, '#f7971e'],     // Naranja dorado
            [0.9, '#ffd200'],     // Amarillo brillante
            [1.0, '#ffffff']      // Blanco puro
        ],
        
        // COLORBAR mejorado
        colorbar: {
            title: {
                text: 'Intensidad<br>Sonora',
                font: { color: '#ffffff', size: 14 }
            },
            titleside: 'right',
            tickfont: { color: '#ffffff', size: 11 },
            thickness: 20,
            len: 0.8,
            x: 1.02,
            bgcolor: 'rgba(0,0,0,0.7)',
            bordercolor: 'rgba(255,255,255,0.3)',
            borderwidth: 1
        },
        
        // LIGHTING PARA SUPERFICIE INTERPOLADA
        lighting: {
            ambient: 0.5,        // Más luz ambiental para ver detalles
            diffuse: 0.9,        // Luz difusa fuerte  
            fresnel: 0.3,        // Efecto fresnel moderado
            specular: 0.8,       // Brillo alto para superficie suave
            roughness: 0.02      // Superficie MUY lisa para interpolación
        },
        
        // CONTOURS proyectados para mejor lectura
        contours: {
            z: {
                show: true,
                start: 0,
                end: 1,
                size: 0.1,
                usecolormap: true,
                highlightcolor: 'rgba(255,255,255,0.8)',
                project: { z: true }
            }
        },
        
        // SURFACE optimizado para performance
        opacity: 0.9,
        showscale: true,
        surfacecolor: mel3DData.colors,
        hovertemplate: '<b>Tiempo:</b> %{x:.2f}s<br>' +
                      '<b>Frecuencia:</b> %{y:.0f} Hz<br>' +
                      '<b>Intensidad:</b> %{z:.3f}<br>' +
                      '<extra></extra>'
    };
    
    const layout = {
        title: {
            text: '🌊 SUPERFICIE SONORA INTERPOLADA - Exploración Musical 3D',
            font: { 
                color: '#ffffff', 
                size: 24,
                family: 'Arial Black' 
            },
            x: 0.5,
            y: 0.96
        },
        
        // SCENE 3D optimizado
        scene: {
            // EJES CON ETIQUETAS DESCRIPTIVAS Y COLORES
            xaxis: {
                title: { 
                    text: '🕐 TIEMPO EN SEGUNDOS',
                    font: { color: '#00ff88', size: 18, family: 'Arial Black' }
                },
                tickfont: { color: '#ffffff', size: 13 },
                gridcolor: 'rgba(0, 255, 136, 0.4)',
                zerolinecolor: 'rgba(0, 255, 136, 0.8)',
                backgroundcolor: 'rgba(0, 30, 20, 0.6)',
                showspikes: true,
                spikesides: false,
                spikecolor: '#00ff88',
                spikethickness: 3
            },
            yaxis: {
                title: { 
                    text: '🎵 FRECUENCIA EN HERTZ (Hz)',
                    font: { color: '#ff6600', size: 18, family: 'Arial Black' }
                },
                tickfont: { color: '#ffffff', size: 13 },
                gridcolor: 'rgba(255, 102, 0, 0.4)',
                zerolinecolor: 'rgba(255, 102, 0, 0.8)',
                backgroundcolor: 'rgba(30, 15, 0, 0.6)',
                showspikes: true,
                spikesides: false,
                spikecolor: '#ff6600',
                spikethickness: 3
            },
            zaxis: {
                title: { 
                    text: '🔊 INTENSIDAD SONORA (dB)',
                    font: { color: '#ff0099', size: 18, family: 'Arial Black' }
                },
                tickfont: { color: '#ffffff', size: 13 },
                gridcolor: 'rgba(255, 0, 153, 0.4)',
                zerolinecolor: 'rgba(255, 0, 153, 0.8)',
                backgroundcolor: 'rgba(30, 0, 20, 0.6)',
                showspikes: true,
                spikesides: false,
                spikecolor: '#ff0099',
                spikethickness: 3
            },
            
            // CÁMARA optimizada para mejor vista inicial
            camera: {
                eye: { x: 1.8, y: 1.8, z: 1.5 },
                center: { x: 0, y: 0, z: 0 },
                up: { x: 0, y: 0, z: 1 }
            },
            
            // ASPECTO Y FONDO
            aspectmode: 'cube',
            bgcolor: 'rgba(0, 0, 0, 0.95)'
        },
        
        // LAYOUT general
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { 
            color: '#ffffff',
            family: 'Arial, sans-serif'
        },
                 margin: { l: 0, r: 0, t: 20, b: 0 },
        
        // HOVER mejorado
        hovermode: 'closest'
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        
        // BOTONES optimizados
        modeBarButtonsToRemove: [
            'pan2d', 'lasso2d', 'select2d', 'autoScale2d'
        ],
        
        // EXPORT de alta calidad
        toImageButtonOptions: {
            format: 'png',
            filename: 'paisaje_sonoro_3d_hd',
            height: 1000,
            width: 1400,
            scale: 2
        },
        
        // PERFORMANCE optimizado
        scrollZoom: true,
        doubleClick: 'reset+autosize'
    };
    
    // RENDERIZAR con callback optimizado
    Plotly.newPlot('melSpectrogram3D', [trace], layout, config)
        .then(function(gd) {
            plot3DRef = gd;
            
            // Eventos optimizados para mejor interactividad
            gd.on('plotly_hover', function(data) {
                gd.style.cursor = 'crosshair';
            });
            
            gd.on('plotly_unhover', function(data) {
                gd.style.cursor = 'default';
            });
        })
        .catch(function(err) {
            console.error('Error renderizando 3D:', err);
        });
}

// Configurar reproductor de audio con marcador 3D
function setupAudioPlayer() {
    if (!currentAudioBlob) return;
    
    audioPlayer = document.getElementById('audioPlayer');
    const audioURL = URL.createObjectURL(currentAudioBlob);
    audioPlayer.src = audioURL;
    
    // Configurar eventos del reproductor
    audioPlayer.addEventListener('timeupdate', updateProgressAndMarker);
    audioPlayer.addEventListener('loadedmetadata', function() {
        document.getElementById('totalTime').textContent = formatTime(audioPlayer.duration);
    });
    
    // Agregar marcador inicial al gráfico 3D
    addTimeMarkerTo3D(0);
}

// Actualizar progreso y marcador 3D
function updateProgressAndMarker() {
    if (!audioPlayer) return;
    
    const currentTime = audioPlayer.currentTime;
    const duration = audioPlayer.duration;
    const progress = (currentTime / duration) * 100;
    
    // Actualizar barra de progreso
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('currentTime').textContent = formatTime(currentTime);
    
    // Actualizar marcador en el gráfico 3D
    addTimeMarkerTo3D(currentTime);
}

// Agregar marcador de tiempo al gráfico 3D
function addTimeMarkerTo3D(currentTime) {
    if (!plot3DRef || !currentAudioData || !currentAudioData.mel_spectrogram_3d) return;
    
    const mel3DData = currentAudioData.mel_spectrogram_3d;
    const maxTime = mel3DData.duration;
    
    // Crear línea vertical en el tiempo actual
    const markerTrace = {
        x: [currentTime, currentTime],
        y: [0, mel3DData.max_freq],
        z: [0, 1],
        type: 'scatter3d',
        mode: 'lines',
        line: {
            color: '#ff0040',
            width: 8
        },
        name: '🎵 Reproduciendo',
        showlegend: false
    };
    
    // Actualizar el gráfico con el marcador
    if (plot3DRef.data.length > 1) {
        // Reemplazar marcador existente
        Plotly.deleteTraces(plot3DRef, 1);
    }
    
    Plotly.addTraces(plot3DRef, markerTrace);
}

// Formatear tiempo mm:ss
function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}



// Utility functions
function showLoading(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
        visualizations.classList.add('hidden');
        trackInfo.classList.add('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

function hideError() {
    errorMessage.classList.add('hidden');
}



// Configurar botones fullscreen Y opciones de visualización
function setupFullscreenButtons(mel3DData) {
    const openBtn = document.getElementById('openFullscreen');
    const closeBtn = document.getElementById('closeFullscreen');
    const fullscreenDiv = document.getElementById('fullscreen3D');
    
    // TIPOS DE VISUALIZACIÓN
    const typeSelect = document.getElementById('viz3DType');
    const colorSelect = document.getElementById('viz3DColor');
    
    openBtn.addEventListener('click', () => {
        fullscreenDiv.style.display = 'block';
        const vizType = typeSelect.value;
        const colorType = colorSelect.value;
        createMelSpectrogram3DWithOptions(mel3DData, vizType, colorType);
        document.body.style.overflow = 'hidden';
    });
    
    closeBtn.addEventListener('click', () => {
        fullscreenDiv.style.display = 'none';
        document.body.style.overflow = 'auto';
    });
    
    // CAMBIAR TIPO DE VISUALIZACIÓN
    typeSelect.addEventListener('change', () => {
        updateVisualization3D(mel3DData);
    });
    
    colorSelect.addEventListener('change', () => {
        updateVisualization3D(mel3DData);
    });
    
    // Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && fullscreenDiv.style.display === 'block') {
            fullscreenDiv.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    });
}

// ACTUALIZAR visualización 3D con opciones
function updateVisualization3D(mel3DData) {
    const vizType = document.getElementById('viz3DType').value;
    const colorType = document.getElementById('viz3DColor').value;
    
    // Actualizar preview
    createMelSpectrogram3DPreviewWithOptions(mel3DData, vizType, colorType);
    
    // Si fullscreen está abierto, actualizar también
    const fullscreenDiv = document.getElementById('fullscreen3D');
    if (fullscreenDiv.style.display === 'block') {
        createMelSpectrogram3DWithOptions(mel3DData, vizType, colorType);
    }
}

// PREVIEW con opciones
function createMelSpectrogram3DPreviewWithOptions(mel3DData, vizType = 'surface', colorType = 'viridis') {
    if (!mel3DData || mel3DData.error) return;
    
    let trace = createTrace3D(mel3DData, vizType, colorType);
    trace.showscale = false;
    trace.opacity = 0.8;
    
    const layout = {
        scene: {
            camera: { eye: { x: 1.2, y: 1.2, z: 1.0 } },
            bgcolor: 'rgba(0,0,0,0.9)'
        },
        margin: { l: 0, r: 0, t: 0, b: 0 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        height: 300
    };
    
    Plotly.newPlot('melSpectrogram3DPreview', [trace], layout, {
        displayModeBar: false, responsive: true
    });
}

// CREAR trace 3D según el tipo
function createTrace3D(mel3DData, vizType, colorType) {
    const colorscales = {
        viridis: 'Viridis',
        plasma: 'Plasma', 
        hot: 'Hot',
        cool: 'Cool'
    };
    
    const baseTrace = {
        x: mel3DData.x_axis,
        y: mel3DData.y_axis,
        z: mel3DData.z_matrix,
        colorscale: colorscales[colorType] || 'Viridis',
        hovertemplate: '<b>🕐 Tiempo:</b> %{x:.2f}s<br>' +
                      '<b>🎵 Frecuencia:</b> %{y:.0f} Hz<br>' +
                      '<b>🔊 Intensidad:</b> %{z:.3f}<br>' +
                      '<extra></extra>'
    };
    
    switch(vizType) {
        case 'surface':
            return {
                ...baseTrace,
                type: 'surface',
                hidesurface: false,
                connectgaps: true,
                lighting: {
                    ambient: 0.5, diffuse: 0.9, fresnel: 0.3,
                    specular: 0.8, roughness: 0.02
                }
            };
            
        case 'wireframe':
            return {
                ...baseTrace,
                type: 'surface',
                hidesurface: true,
                showscale: false,
                contours: {
                    x: { show: true, color: '#ffffff', width: 2 },
                    y: { show: true, color: '#ffffff', width: 2 },
                    z: { show: true, color: '#ffffff', width: 2 }
                }
            };
            
        case 'scatter3d':
            // Convertir matriz a puntos individuales para scatter3d
            const points = [];
            for (let i = 0; i < mel3DData.z_matrix.length; i++) {
                for (let j = 0; j < mel3DData.z_matrix[i].length; j++) {
                    if (mel3DData.z_matrix[i][j] > 0.1) { // Solo puntos significativos
                        points.push({
                            x: mel3DData.x_axis[j],
                            y: mel3DData.y_axis[i], 
                            z: mel3DData.z_matrix[i][j],
                            intensity: mel3DData.z_matrix[i][j]
                        });
                    }
                }
            }
            
            return {
                x: points.map(p => p.x),
                y: points.map(p => p.y),
                z: points.map(p => p.z),
                type: 'scatter3d',
                mode: 'markers',
                marker: {
                    size: 3,
                    color: points.map(p => p.intensity),
                    colorscale: colorscales[colorType],
                    opacity: 0.8
                },
                hovertemplate: baseTrace.hovertemplate
            };
            
        default:
            return { ...baseTrace, type: 'surface' };
    }
}

// FULLSCREEN con opciones
function createMelSpectrogram3DWithOptions(mel3DData, vizType = 'surface', colorType = 'viridis') {
    if (!mel3DData || mel3DData.error) return;
    
    const trace = createTrace3D(mel3DData, vizType, colorType);
    
    // Layout completo para fullscreen
    const layout = {
        title: {
            text: `🌊 SUPERFICIE SONORA ${vizType.toUpperCase()} - ${colorType.toUpperCase()}`,
            font: { color: '#ffffff', size: 24, family: 'Arial Black' },
            x: 0.5, y: 0.96
        },
        scene: {
            xaxis: {
                title: { text: '🕐 TIEMPO EN SEGUNDOS', font: { color: '#00ff88', size: 18, family: 'Arial Black' }},
                tickfont: { color: '#ffffff', size: 13 }
            },
            yaxis: {
                title: { text: '🎵 FRECUENCIA EN HERTZ (Hz)', font: { color: '#ff6600', size: 18, family: 'Arial Black' }},
                tickfont: { color: '#ffffff', size: 13 }
            },
            zaxis: {
                title: { text: '🔊 INTENSIDAD SONORA (dB)', font: { color: '#ff0099', size: 18, family: 'Arial Black' }},
                tickfont: { color: '#ffffff', size: 13 }
            },
            camera: { eye: { x: 1.8, y: 1.8, z: 1.5 }},
            bgcolor: 'rgba(5,5,15,0.95)'
        },
        paper_bgcolor: 'rgba(0,0,0,1)',
        margin: { l: 0, r: 80, t: 40, b: 0 }
    };
    
    Plotly.newPlot('melSpectrogram3D', [trace], layout, {
        responsive: true, displayModeBar: true, scrollZoom: true
    }).then(function(gd) {
        plot3DRef = gd;
    });
} 