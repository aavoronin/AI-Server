from pathlib import Path
from typing import Optional
import logging
from .ModelBase import ModelBase

logger = logging.getLogger(__name__)


class ModelFactory:
    """Factory to manage model instances, ensuring only one is loaded at a time."""
    _current_model: Optional[ModelBase] = None
    _current_model_id: Optional[str] = None

    @classmethod
    def get_model(cls, model_id: str, cache_dir: str) -> ModelBase:
        if cls._current_model_id == model_id and cls._current_model is not None:
            return cls._current_model

        if cls._current_model is not None:
            logger.info(f"Unloading previous model: {cls._current_model_id}")
            cls._current_model.unload()
            cls._current_model = None
            cls._current_model_id = None

        model_class = cls._determine_model_class(model_id)
        cls._current_model = model_class(model_id, cache_dir)
        cls._current_model_id = model_id

        try:
            cls._current_model.load()
        except Exception as e:
            logger.error(f"Failed to load model {model_id}, incrementing fails.")
            cls._current_model.increment_fails()
            raise e

        return cls._current_model

    @classmethod
    def _determine_model_class(cls, model_id: str):
        model_id_lower = model_id.lower()
        if "gguf" in model_id_lower or "ggml" in model_id_lower:
            from .GGUFTextToTextModel import GGUFTextToTextModel
            return GGUFTextToTextModel
        elif "gptq" in model_id_lower:
            from .GPTQTextToTextModel import GPTQTextToTextModel
            return GPTQTextToTextModel
        elif "onnx" in model_id_lower:
            from .ONNXTextToTextModel import ONNXTextToTextModel
            return ONNXTextToTextModel
        elif "mlx" in model_id_lower:
            from .MLXTextToTextModel import MLXTextToTextModel
            return MLXTextToTextModel
        else:
            from .TransformersTextToTextModel import TransformersTextToTextModel
            return TransformersTextToTextModel