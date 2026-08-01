from .TextToTextModel import TextToTextModel
import logging

logger = logging.getLogger(__name__)


class ONNXTextToTextModel(TextToTextModel):
    def load(self):
        raise NotImplementedError("ONNX loading requires onnxruntime and specific conversion.")

    def unload(self):
        pass

    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError("ONNX generation not fully implemented in this stub.")