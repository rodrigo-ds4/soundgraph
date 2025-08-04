# SoundGraph

**Professional Audio Analysis and Visualization Platform**

SoundGraph is a web-based audio analysis tool designed for DJs and music professionals. It provides advanced signal processing capabilities to generate professional-grade audio visualizations similar to those found in industry-standard software like Serato DJ, Virtual DJ, Traktor Pro, and Ableton Live.

## Features

### Audio Visualizations
- **Multi-frequency Waveform Analysis** - Color-coded waveform representation with frequency band separation (Bass/Red, Mids/Green, Highs/Blue)
- **Mel-Spectrogram Generation** - AI-style audio-to-image representation compatible with generative audio models
- **Real-time Spectrogram** - Frequency domain analysis with time-based progression
- **3D Audio Landscape** - Three-dimensional topographic representation of audio data

### Technical Capabilities
- **Automatic BPM Detection** - Real-time tempo analysis using onset detection algorithms
- **Multi-format Support** - MP3, WAV, M4A, FLAC audio file processing
- **RESTful API** - FastAPI-based backend with JSON responses
- **Real-time Processing** - Efficient audio analysis with optimized algorithms

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/soundgraph.git
cd soundgraph
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Start the application**
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

5. **Access the application**
```
http://localhost:8001
```

## Usage

### Web Interface
1. Navigate to the web interface
2. Upload audio file via drag-and-drop or file selector
3. Wait for analysis processing (typically 2-5 seconds)
4. View generated visualizations and BPM analysis

### Desktop Application
For advanced 3D visualizations:
```bash
python run_desktop.py
```

## Technical Architecture

### Backend Stack
- **FastAPI** - High-performance Python web framework
- **Librosa** - Audio signal analysis and music information retrieval
- **NumPy/SciPy** - Numerical computing and signal processing
- **Matplotlib** - Static visualization generation
- **Plotly** - Interactive web-based visualizations
- **PyVista** - 3D scientific visualization (desktop app)

### Frontend Stack
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework dependencies
- **Plotly.js** - Interactive visualization rendering
- **Web Audio API** - Client-side audio handling

### Audio Processing Pipeline
1. **File Input** - Multi-format audio file handling with ffmpeg integration
2. **Signal Processing** - Librosa-based audio analysis with STFT computation
3. **Feature Extraction** - BPM detection, frequency analysis, onset detection
4. **Visualization Generation** - Multiple rendering engines for different output types
5. **Web Delivery** - JSON API responses with embedded visualization data

## Project Structure

```
soundgraph/
├── main.py                    # FastAPI application entry point
├── audio_processor.py         # Core audio analysis engine
├── audio_journey_3d.py        # 3D visualization processing
├── soundgraph_desktop.py      # Desktop GUI application
├── run_desktop.py             # Desktop application launcher
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web interface template
├── static/
│   ├── style.css            # Application styling
│   └── script.js            # Frontend JavaScript
└── README_DESKTOP.md        # Desktop application documentation
```

## API Endpoints

### POST /upload
Processes audio file and returns analysis data.

**Request:** Multipart form data with audio file
**Response:** JSON with visualizations, BPM, and metadata

### GET /health
Application health check endpoint.

**Response:** JSON status indicator

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --port 8001
```

### Running Tests
```bash
python test_pyvista.py  # Test 3D visualization capabilities
```

## Configuration

### Audio Processing Parameters
- Sample Rate: 22,050 Hz (optimized for music analysis)
- FFT Window: 2048 samples
- Hop Length: 512 samples
- Mel Bands: 128 (for spectrograms)

### Performance Optimization
- Efficient memory management for large audio files
- Parallel processing for multiple visualization types
- Caching for repeated analysis operations

## Troubleshooting

### Common Issues

**ffmpeg not found**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
Download from https://ffmpeg.org/download.html
```

**Port already in use**
```bash
# Change port in main.py or use command line
uvicorn main:app --port 8002
```

**Memory issues with large files**
- Limit audio file size to 10MB for optimal performance
- Use WAV format for fastest processing
- Ensure sufficient RAM (4GB+ recommended)

## Future Development

### Planned Features
- Machine learning-based song similarity analysis
- Advanced beat detection and rhythm analysis
- Scientific audio metrics and reporting
- Multi-track comparison and overlay
- Export capabilities (JSON, CSV, PNG formats)

### Technical Roadmap
- WebAssembly integration for client-side processing
- GPU acceleration for large file analysis
- Real-time audio stream processing
- Plugin architecture for custom visualizations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with appropriate tests
4. Submit a pull request with detailed description

## License

MIT License - Open source software for educational and commercial use.

## Technical Support

For technical issues, please refer to the troubleshooting section above or create an issue in the project repository. 