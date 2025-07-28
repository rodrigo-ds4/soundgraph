from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import tempfile
from audio_processor import AudioProcessor
from audio_journey_3d import generate_audio_journey_3d

app = FastAPI(title="SoundGraph DJ", description="Análisis visual de audio para DJs")

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicializar procesador de audio
audio_processor = AudioProcessor()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal minimalista"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Subir archivo de audio y procesarlo"""
    try:
        # Validar formato
        if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.flac')):
            return JSONResponse(
                status_code=400, 
                content={"error": "Formato no soportado. Usa MP3, WAV, M4A o FLAC"}
            )
        
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Procesar audio
        result = await audio_processor.process_audio(tmp_path, file.filename)
        
        # Limpiar archivo temporal
        os.unlink(tmp_path)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error procesando audio: {str(e)}"}
        )

@app.post("/journey")
async def generate_journey_3d(file: UploadFile = File(...)):
    """
    🚀 NUEVO: Generar viaje 3D completo por una canción
    Con separación de graves, medios y agudos + navegación temporal
    """
    try:
        # Validar formato
        if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.flac')):
            return JSONResponse(
                status_code=400, 
                content={"error": "Formato no soportado para viaje 3D. Usa MP3, WAV, M4A o FLAC"}
            )
        
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        print(f"🎵 Iniciando viaje 3D para: {file.filename}")
        
        # Generar viaje 3D (1 minuto por defecto)
        journey_result = generate_audio_journey_3d(tmp_path, duration_minutes=1.0)
        
        # Limpiar archivo temporal
        os.unlink(tmp_path)
        
        if journey_result['success']:
            return JSONResponse({
                "success": True,
                "filename": file.filename,
                "duration": journey_result['duration'],
                "html_3d": journey_result['html_3d'],
                "sync_data": journey_result['sync_data'],
                "journey_stats": journey_result['journey_stats'],
                "message": f"🏔️ Viaje 3D generado: {journey_result['journey_stats']['total_frames']} frames temporales"
            })
        else:
            return JSONResponse({
                "success": False,
                "error": journey_result['error']
            }, status_code=500)
            
    except Exception as e:
        # Limpiar en caso de error
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass
        
        return JSONResponse({
            "success": False,
            "error": f"Error procesando viaje 3D: {str(e)}"
        }, status_code=500)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "SoundGraph DJ API funcionando"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True) 