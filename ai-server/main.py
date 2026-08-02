from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import json
import shutil
import subprocess
from datetime import datetime
from typing import List, Optional
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import ServerConfig
from model_filter import ModelFilter
from model_manager import ModelManager
from model_engines.ModelFactory import ModelFactory

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


def ensure_model_cached(model_id: str, cache_folder: str, hf_token_path: str) -> bool:
    """Ensure the model is cached, downloading it if necessary."""
    model_folder_name = model_id.replace("/", "_")
    model_dir = Path(cache_folder) / model_folder_name
    model_dir.mkdir(parents=True, exist_ok=True)

    usage_file = model_dir / "model_usage.json"
    is_cached = False

    # Initialize usage_data with defaults to prevent UnboundLocalError
    usage_data = {
        "model_id": model_id,
        "is_cached": False,
        "last_used": None,
        "last_cached": None,
        "last_uncached": None,
        "num_used": 0,
        "num_fails": 0
    }

    if usage_file.exists():
        with open(usage_file, 'r') as f:
            usage_data = json.load(f)
            is_cached = usage_data.get("is_cached", False)

    if not is_cached:
        token = None
        token_file = Path(hf_token_path)
        if token_file.exists():
            token = token_file.read_text().strip()

        env = os.environ.copy()
        if token:
            env["HF_TOKEN"] = token

        try:
            subprocess.run(
                ["huggingface-cli", "download", model_id, "--local-dir", str(model_dir)],
                env=env,
                check=True,
                capture_output=True,
                text=True
            )
            usage_data["is_cached"] = True
            usage_data["last_cached"] = datetime.now().isoformat()
            with open(usage_file, 'w') as f:
                json.dump(usage_data, f, indent=2)
            return True
        except subprocess.CalledProcessError as e:
            usage_data["num_fails"] = usage_data.get("num_fails", 0) + 1
            with open(usage_file, 'w') as f:
                json.dump(usage_data, f, indent=2)
            return False
    return True


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


@app.get("/models/{model_id:path}")
async def get_model_by_id(model_id: str):
    """Get a specific model by ID"""
    if model_manager is None:
        raise HTTPException(status_code=500, detail="Model manager not initialized")

    models = model_manager.get_all_models()
    for model in models:
        if model.get('model_id') == model_id:
            return model

    raise HTTPException(status_code=404, detail=f"Model {model_id} not found")


@app.post("/models/{model_id:path}/cache")
async def cache_model(model_id: str):
    """Cache a model by downloading it to the cache folder."""
    if ensure_model_cached(model_id, config.cache_folder_path, config.hf_token_path):
        model_dir = Path(config.cache_folder_path) / model_id.replace("/", "_")
        with open(model_dir / "model_usage.json", 'r') as f:
            return json.load(f)
    raise HTTPException(status_code=500, detail="Failed to download model")


@app.post("/models/{model_id:path}/uncache")
async def uncache_model(model_id: str):
    """Uncache a model by removing its files but keeping usage tracking."""
    model_folder_name = model_id.replace("/", "_")
    model_dir = Path(config.cache_folder_path) / model_folder_name

    if not model_dir.exists():
        raise HTTPException(status_code=404, detail="Model folder not found")

    usage_file = model_dir / "model_usage.json"
    if usage_file.exists():
        with open(usage_file, 'r') as f:
            usage_data = json.load(f)
    else:
        usage_data = {
            "model_id": model_id,
            "is_cached": False,
            "last_used": None,
            "last_cached": None,
            "last_uncached": None,
            "num_used": 0,
            "num_fails": 0
        }

    for item in model_dir.iterdir():
        if item.name != "model_usage.json":
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

    usage_data["is_cached"] = False
    usage_data["last_uncached"] = datetime.now().isoformat()

    with open(usage_file, 'w') as f:
        json.dump(usage_data, f, indent=2)

    return usage_data


@app.get("/models/cached")
async def list_cached_models():
    """List all cached models and their status."""
    cache_dir = Path(config.cache_folder_path)
    cached_models = []

    if cache_dir.exists():
        for item in cache_dir.iterdir():
            if item.is_dir():
                usage_file = item / "model_usage.json"
                if usage_file.exists():
                    with open(usage_file, 'r') as f:
                        usage_data = json.load(f)
                        cached_models.append(usage_data)

    return {
        "count": len(cached_models),
        "cached_models": cached_models
    }


@app.post("/models/{model_id:path}/generate")
async def generate_text(model_id: str, request: dict):
    """Process a text-to-text generation request."""
    if model_manager is None:
        raise HTTPException(status_code=500, detail="Model manager not initialized")

    if not ensure_model_cached(model_id, config.cache_folder_path, config.hf_token_path):
        raise HTTPException(status_code=500, detail="Failed to cache model")

    try:
        model = ModelFactory.get_model(model_id, config.cache_folder_path)
        prompt = request.get("prompt", "")
        max_new_tokens = request.get("max_new_tokens")
        temperature = request.get("temperature", 0.7)

        kwargs = {}
        if max_new_tokens is not None:
            kwargs["max_new_tokens"] = max_new_tokens
        if temperature is not None:
            kwargs["temperature"] = temperature

        result = model.safe_generate(prompt, **kwargs)
        return {"model_id": model_id, "generated_text": result}
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting server on {config.host}:{config.port}")
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level="info"
    )