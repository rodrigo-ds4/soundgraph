from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn
import os
import tempfile
import logging
from audio_processor import AudioProcessor
from config import ServerConfig, get_environment_config

# Get environment configuration
audio_config, server_config = get_environment_config()

# Configure logging
logging.basicConfig(
    level=getattr(logging, server_config.LOG_LEVEL),
    format=server_config.LOG_FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="SoundGraph", 
    description="Professional audio analysis and visualization platform for DJs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add GZip middleware for compression
app.add_middleware(GZipMiddleware, minimum_size=audio_config.COMPRESSION_LEVEL * 100)

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicializar procesador de audio
audio_processor = AudioProcessor()

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🎵 SoundGraph Audio Analysis Platform starting up...")
    logger.info(f"Environment: {server_config.LOG_LEVEL}")
    logger.info(f"Max file size: {audio_config.MAX_FILE_SIZE / 1024 / 1024:.0f}MB")
    
@app.on_event("shutdown") 
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("🎵 SoundGraph shutting down...")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal minimalista"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Subir archivo de audio y procesarlo"""
    try:
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Validar que se subió un archivo
        if not file.filename:
            raise HTTPException(status_code=400, detail="No se subió ningún archivo")
        
        # Validar formato
        allowed_formats = ('.mp3', '.wav', '.m4a', '.flac')
        if not file.filename.lower().endswith(allowed_formats):
            raise HTTPException(
                status_code=400, 
                detail=f"Formato no soportado. Formatos permitidos: {', '.join(allowed_formats)}"
            )
        
        # Validar tamaño del archivo
        content = await file.read()
        max_size = audio_config.MAX_FILE_SIZE
        if len(content) > max_size:
            raise HTTPException(
                status_code=413, 
                detail=f"Archivo muy grande. Tamaño máximo: {max_size / 1024 / 1024:.0f}MB. Tu archivo: {len(content) / 1024 / 1024:.1f}MB"
            )
        
        # Validar que el archivo no esté vacío
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        # Guardar archivo temporal
        file_extension = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        logger.info(f"Temporary file created: {tmp_path}")
        
        # Procesar audio
        result = await audio_processor.process_audio(tmp_path, file.filename)
        
        # Limpiar archivo temporal
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
            logger.info(f"Temporary file cleaned: {tmp_path}")
        
        if result.get("success", False):
            logger.info(f"Audio processing completed successfully for: {file.filename}")
            return JSONResponse(content=result)
        else:
            logger.error(f"Audio processing failed for: {file.filename}")
            raise HTTPException(status_code=500, detail=result.get("error", "Error desconocido"))
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "SoundGraph DJ API funcionando"}

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=server_config.HOST, 
        port=server_config.PORT, 
        reload=server_config.RELOAD,
        log_level=server_config.LOG_LEVEL.lower(),
        timeout_keep_alive=server_config.KEEP_ALIVE
    ) 