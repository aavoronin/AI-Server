from .TextToTextModel import TextToTextModel
import logging

logger = logging.getLogger(__name__)


class GPTQTextToTextModel(TextToTextModel):
    def load(self):
        raise NotImplementedError("GPTQ loading requires auto-gptq and specific CUDA setup.")

    def unload(self):
        pass

    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("GPTQ generation not fully implemented in this stub.")