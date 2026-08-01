from .TextToTextModel import TextToTextModel
import logging

logger = logging.getLogger(__name__)


class GGUFTextToTextModel(TextToTextModel):
    def __init__(self, model_id: str, cache_dir: str):
        super().__init__(model_id, cache_dir)
        self.model = None
        self.tokenizer = None

    def load(self):
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            logger.info(f"Loading GGUF model with Transformers: {self.model_id}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True
            )
            self.is_loaded = True
            logger.info(f"Successfully loaded GGUF {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to load GGUF model {self.model_id}: {e}")
            raise

    def unload(self):
        if self.model is not None:
            del self.model
        if self.tokenizer is not None:
            del self.tokenizer
        import gc
        gc.collect()
        self.is_loaded = False
        logger.info(f"Unloaded GGUF {self.model_id}")

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")

        max_new_tokens = kwargs.get("max_new_tokens", 32768)
        messages = [{"role": "user", "content": prompt}]

        try:
            text = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=True
            )
            model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=max_new_tokens
            )
            output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

            try:
                # rindex finding 151668 (</think>)
                index = len(output_ids) - output_ids[::-1].index(151668)
            except ValueError:
                index = 0

            thinking_content = self.tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
            content = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

            if thinking_content:
                return f"Thinking: {thinking_content}\n\nContent: {content}"
            return content
        except Exception as e:
            logger.error(f"Generation failed for GGUF {self.model_id}: {e}")
            raise