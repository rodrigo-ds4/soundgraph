"""
Configuration settings for SoundGraph audio processing
Optimized parameters for performance and quality balance
"""
import os
from typing import Dict, Any

class AudioConfig:
    """Audio processing configuration"""
    
    # Sample rates for different quality levels
    SAMPLE_RATE_HIGH = 44100     # High quality for studio files
    SAMPLE_RATE_STANDARD = 22050 # Standard quality (default)
    SAMPLE_RATE_FAST = 11025     # Fast processing for large files
    
    # Processing parameters
    N_FFT = 2048
    HOP_LENGTH_HIGH = 256        # High resolution
    HOP_LENGTH_STANDARD = 512    # Standard resolution
    HOP_LENGTH_FAST = 1024       # Fast processing
    
    # Mel-spectrogram settings
    N_MELS_HIGH = 256           # High detail spectrograms
    N_MELS_STANDARD = 128       # Standard spectrograms
    N_MELS_FAST = 64            # Quick spectrograms
    
    # File handling
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
    TEMP_DIR = os.path.join(os.getcwd(), "temp")
    
    # Performance settings
    ENABLE_GPU_ACCELERATION = False  # Enable if CUDA available
    MAX_CONCURRENT_PROCESSES = 2     # Limit concurrent audio processing
    CACHE_RESULTS = True             # Cache processed results
    COMPRESSION_LEVEL = 6            # GZip compression level (1-9)
    
    @classmethod
    def get_config_for_file_size(cls, file_size_bytes: int) -> Dict[str, Any]:
        """
        Get optimal configuration based on file size
        Automatic quality/speed balancing
        """
        file_size_mb = file_size_bytes / (1024 * 1024)
        
        if file_size_mb > 15:  # Large files - prioritize speed
            return {
                'sample_rate': cls.SAMPLE_RATE_FAST,
                'hop_length': cls.HOP_LENGTH_FAST,
                'n_mels': cls.N_MELS_FAST,
                'quality_level': 'fast',
                'processing_message': 'Optimizado para velocidad (archivo grande)'
            }
        elif file_size_mb > 5:  # Medium files - balanced
            return {
                'sample_rate': cls.SAMPLE_RATE_STANDARD,
                'hop_length': cls.HOP_LENGTH_STANDARD,
                'n_mels': cls.N_MELS_STANDARD,
                'quality_level': 'standard',
                'processing_message': 'Calidad estándar (balanceado)'
            }
        else:  # Small files - prioritize quality
            return {
                'sample_rate': cls.SAMPLE_RATE_HIGH,
                'hop_length': cls.HOP_LENGTH_HIGH,
                'n_mels': cls.N_MELS_HIGH,
                'quality_level': 'high',
                'processing_message': 'Alta calidad (archivo pequeño)'
            }

class ServerConfig:
    """Server and API configuration"""
    
    # Server settings
    HOST = "0.0.0.0"
    PORT = 8001
    DEBUG = False
    RELOAD = True
    
    # Security settings
    ALLOWED_ORIGINS = ["*"]  # Configure for production
    MAX_REQUEST_SIZE = 30 * 1024 * 1024  # 30MB (buffer over file limit)
    
    # Performance settings
    WORKERS = 1  # Single worker for development
    KEEP_ALIVE = 65
    TIMEOUT = 120  # 2 minutes timeout for audio processing
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Environment-based configuration
def get_environment_config():
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        ServerConfig.DEBUG = False
        ServerConfig.RELOAD = False
        ServerConfig.LOG_LEVEL = "WARNING"
        AudioConfig.CACHE_RESULTS = True
        AudioConfig.COMPRESSION_LEVEL = 9
    
    elif env == "development":
        ServerConfig.DEBUG = True
        ServerConfig.RELOAD = True
        ServerConfig.LOG_LEVEL = "INFO"
        AudioConfig.CACHE_RESULTS = False
        AudioConfig.COMPRESSION_LEVEL = 1
    
    return AudioConfig, ServerConfig
