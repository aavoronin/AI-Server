from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List, Optional
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import ServerConfig, ModelFilter
from models import ModelManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize configuration and app
config = ServerConfig()
app = FastAPI(
    title="AI Model Server",
    description="Server for managing and filtering AI models",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model manager
try:
    model_manager = ModelManager(config.models_csv_path)
    logger.info("Model manager initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize model manager: {e}")
    model_manager = None


@app.get("/")
async def root():
    """Root endpoint - check if server is running"""
    return {
        "status": "online",
        "message": "AI Model Server is running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": model_manager is not None,
        "total_models": len(model_manager.get_all_models()) if model_manager else 0
    }


@app.get("/models")
async def get_all_models():
    """Get all models"""
    if model_manager is None:
        raise HTTPException(status_code=500, detail="Model manager not initialized")

    models = model_manager.get_all_models()
    return {
        "count": len(models),
        "models": models
    }


@app.get("/models/filter")
async def filter_models(
        # Modality filters
        input_modalities: Optional[str] = Query(
            None,
            description="Comma-separated input modalities (e.g., 'Text,Image')"
        ),
        output_modalities: Optional[str] = Query(
            None,
            description="Comma-separated output modalities (e.g., 'Image,Audio')"
        ),
        # Numeric range filters
        model_size_from: Optional[int] = Query(None, description="Minimum model size"),
        model_size_to: Optional[int] = Query(None, description="Maximum model size"),
        input_tokens_from: Optional[int] = Query(None, description="Minimum input tokens"),
        input_tokens_to: Optional[int] = Query(None, description="Maximum input tokens"),
        output_tokens_from: Optional[int] = Query(None, description="Minimum output tokens"),
        output_tokens_to: Optional[int] = Query(None, description="Maximum output tokens"),
        downloads_from: Optional[int] = Query(None, description="Minimum downloads"),
        downloads_to: Optional[int] = Query(None, description="Maximum downloads"),
        likes_from: Optional[int] = Query(None, description="Minimum likes"),
        likes_to: Optional[int] = Query(None, description="Maximum likes"),
        size_b_from: Optional[int] = Query(None, description="Minimum SizeB"),
        size_b_to: Optional[int] = Query(None, description="Maximum SizeB"),
):
    """
    Filter models based on modalities and numeric ranges

    All parameters are optional. No parameters returns all models.

    Examples:
    - /models/filter?input_modalities=Text&output_modalities=Text
    - /models/filter?input_modalities=Text,Image&output_modalities=Image&downloads_from=1000&downloads_to=100000
    - /models/filter?model_size_from=100000&model_size_to=10000000
    """
    if model_manager is None:
        raise HTTPException(status_code=500, detail="Model manager not initialized")

    try:
        filtered_models = model_manager.filter_models(
            input_modalities=input_modalities,
            output_modalities=output_modalities,
            model_size_from=model_size_from,
            model_size_to=model_size_to,
            input_tokens_from=input_tokens_from,
            input_tokens_to=input_tokens_to,
            output_tokens_from=output_tokens_from,
            output_tokens_to=output_tokens_to,
            downloads_from=downloads_from,
            downloads_to=downloads_to,
            likes_from=likes_from,
            likes_to=likes_to,
            size_b_from=size_b_from,
            size_b_to=size_b_to,
        )

        return {
            "count": len(filtered_models),
            "filters": {
                "input_modalities": input_modalities,
                "output_modalities": output_modalities,
                "model_size": {"from": model_size_from, "to": model_size_to},
                "downloads": {"from": downloads_from, "to": downloads_to},
                "likes": {"from": likes_from, "to": likes_to},
            },
            "models": filtered_models
        }
    except Exception as e:
        logger.error(f"Error filtering models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models/{model_id}")
async def get_model_by_id(model_id: str):
    """Get a specific model by ID"""
    if model_manager is None:
        raise HTTPException(status_code=500, detail="Model manager not initialized")

    models = model_manager.get_all_models()
    for model in models:
        if model.get('model_id') == model_id:
            return model

    raise HTTPException(status_code=404, detail=f"Model {model_id} not found")


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {config.host}:{config.port}")
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info"
    )