import json
from pathlib import Path
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class ModelBase(ABC):
    """Base class for all AI models."""
    _debug_printed_models = set()

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

    def safe_generate(self, prompt: str, **kwargs) -> str:
        try:
            return self.generate(prompt, **kwargs)
        except Exception as e:
            self._print_debug_info()
            raise e

    def _print_debug_info(self):
        if self.model_id in self._debug_printed_models:
            return
        self._debug_printed_models.add(self.model_id)

        print(f"\n--- DEBUG INFO FOR {self.model_id} ---")
        readme_path = self.model_path / "README.md"
        if readme_path.exists():
            print("\n[README.md]")
            try:
                content = readme_path.read_text()
                print(content[:4000])
            except Exception as e:
                print(f"Error reading README.md: {e}")

        for json_file in self.model_path.glob("*.json"):
            if json_file.name == "model_usage.json":
                continue
            try:
                if json_file.stat().st_size <= 5120:
                    print(f"\n[{json_file.name}]")
                    print(json_file.read_text())
            except Exception as e:
                print(f"Error reading {json_file.name}: {e}")
        print("--- END DEBUG INFO ---\n")

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

    def increment_init_success(self):
        """Increment num_init_successes in model_usage.json if initialization succeeds."""
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {}

            data["num_init_successes"] = data.get("num_init_successes", 0) + 1

            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to increment init successes: {e}")