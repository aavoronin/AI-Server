from .TextToTextModel import TextToTextModel
import logging

logger = logging.getLogger(__name__)


class GGUFTextToTextModel(TextToTextModel):
    def __init__(self, model_id: str, cache_dir: str):
        super().__init__(model_id, cache_dir)
        self.llm = None

    def load(self):
        try:
            from llama_cpp import Llama

            logger.info(f"Loading GGUF model: {self.model_id}")
            gguf_files = list(self.model_path.glob("*.gguf"))
            if not gguf_files:
                raise FileNotFoundError(f"No .gguf file found in {self.model_path}")

            gguf_path = str(gguf_files[0])

            self.llm = Llama(
                model_path=gguf_path,
                n_gpu_layers=-1,
                n_ctx=4096,
                verbose=False
            )
            self.is_loaded = True
            logger.info(f"Successfully loaded GGUF {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to load GGUF model {self.model_id}: {e}")
            raise

    def unload(self):
        if self.llm is not None:
            del self.llm
        import gc
        gc.collect()
        self.is_loaded = False
        logger.info(f"Unloaded GGUF {self.model_id}")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")

        max_tokens = kwargs.get("max_new_tokens", 2048)
        try:
            result = self.llm(
                prompt,
                max_tokens=max_tokens,
                echo=False
            )
            return result["choices"][0]["text"]
        except Exception as e:
            logger.error(f"Generation failed for GGUF {self.model_id}: {e}")
            raise