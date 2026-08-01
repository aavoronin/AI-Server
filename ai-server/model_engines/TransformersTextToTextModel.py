from .TextToTextModel import TextToTextModel
import logging

logger = logging.getLogger(__name__)


class TransformersTextToTextModel(TextToTextModel):
    def __init__(self, model_id: str, cache_dir: str):
        super().__init__(model_id, cache_dir)
        self.pipeline = None
        self.tokenizer = None
        self.model = None

    def load(self):
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

            logger.info(f"Loading Transformers model: {self.model_id}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True
            )

            # Do not pass device=device when device_map="auto" is used
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer
            )
            self.is_loaded = True
            logger.info(f"Successfully loaded {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to load Transformers model {self.model_id}: {e}")
            raise

    def unload(self):
        if self.model is not None:
            del self.model
        if self.pipeline is not None:
            del self.pipeline
        if self.tokenizer is not None:
            del self.tokenizer
        import gc
        gc.collect()
        self.is_loaded = False
        logger.info(f"Unloaded {self.model_id}")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")

        max_new_tokens = kwargs.get("max_new_tokens", 2048)

        try:
            result = self.pipeline(
                prompt,
                max_new_tokens=max_new_tokens,
                do_sample=kwargs.get("do_sample", True),
                temperature=kwargs.get("temperature", 0.7)
            )
            return result[0]["generated_text"]
        except Exception as e:
            logger.error(f"Generation failed for {self.model_id}: {e}")
            raise