import json
from pathlib import Path
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class ModelBase(ABC):
    """Base class for all AI models."""

    def __init__(self, model_id: str, cache_dir: str):
        self.model_id = model_id
        self.cache_dir = Path(cache_dir)
        self.model_folder_name = model_id.replace("/", "_")
        self.model_path = self.cache_dir / self.model_folder_name
        self.usage_file = self.model_path / "model_usage.json"
        self.is_loaded = False

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        pass

    def increment_fails(self):
        """Increment num_fails in model_usage.json if initialization fails."""
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"num_fails": 0}

            data["num_fails"] = data.get("num_fails", 0) + 1

            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to increment fails: {e}")