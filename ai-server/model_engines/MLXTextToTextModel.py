from .TextToTextModel import TextToTextModel
import logging

logger = logging.getLogger(__name__)


class MLXTextToTextModel(TextToTextModel):
    def load(self):
        raise NotImplementedError("MLX loading is only supported on Apple Silicon.")

    def unload(self):
        pass

    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("MLX generation not fully implemented in this stub.")