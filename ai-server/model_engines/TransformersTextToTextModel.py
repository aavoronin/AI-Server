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

            # Patch config.json if model_type is qwen3 and transformers doesn't support it
            config_path = self.model_path / "config.json"
            if config_path.exists():
                import json
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                    if config_data.get("model_type") == "qwen3":
                        logger.info(f"Patching config.json model_type from qwen3 to qwen2 for {self.model_id}")
                        config_data["model_type"] = "qwen2"
                        with open(config_path, 'w') as f:
                            json.dump(config_data, f)
                except Exception as e:
                    logger.warning(f"Could not patch config.json for {self.model_id}: {e}")

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
            self.increment_init_success()

        except Exception as e:
            logger.error(f"Failed to load Transformers model {self.model_id}: {e}")
            self.increment_fails()
            self._print_debug_info()
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

    def register_common_prompt(self, prompt: str):
        super().register_common_prompt(prompt)
        if not self.use_llama_cpp and self.model is not None:
            import torch
            # Precalculate by running a forward pass to extract past_key_values
            messages = [{"role": "user", "content": prompt}]
            text = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
            with torch.no_grad():
                outputs = self.model(**inputs, use_cache=True)

            self.common_prompt_past_key_values = outputs.past_key_values
            self.common_prompt_input_length = inputs.input_ids.shape[1]
            logger.info(
                f"Precalculated common prompt for {self.model_id} "
                f"({self.common_prompt_input_length} tokens)"
            )

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded")

        # Set max_new_tokens to 8192 for Gemma-3 models as per specification
        model_id_lower = self.model_id.lower()
        default_max_tokens = 8192 if "gemma-3" in model_id_lower else 2048
        max_new_tokens = kwargs.get("max_new_tokens", default_max_tokens)

        try:
            if self.use_llama_cpp:
                # This branch is theoretically unreachable for this class,
                # but kept for structural consistency if mixed
                pass
            else:
                # Check if we can reuse the precalculated past_key_values
                if (hasattr(self, 'common_prompt_past_key_values') and
                        self.common_prompt_past_key_values is not None and
                        prompt.startswith(self.registered_common_prompt)):

                    import torch
                    remaining_prompt = prompt[len(self.registered_common_prompt):]

                    # Tokenize the remaining part without special tokens
                    # since they were already processed in the common prompt
                    remaining_inputs = self.tokenizer(
                        [remaining_prompt], return_tensors="pt", add_special_tokens=False
                    ).to(self.model.device)

                    generated_ids = self.model.generate(
                        input_ids=remaining_inputs.input_ids,
                        past_key_values=self.common_prompt_past_key_values,
                        max_new_tokens=max_new_tokens,
                        temperature=kwargs.get("temperature", 0.7),
                        repetition_penalty=kwargs.get("repeat_penalty", 1.1),
                        do_sample=kwargs.get("do_sample", True),
                        use_cache=True
                    )

                    # Decode only the newly generated tokens
                    output_ids = generated_ids[0][remaining_inputs.input_ids.shape[1]:].tolist()
                    content = self.tokenizer.decode(
                        output_ids, skip_special_tokens=True
                    ).strip("\n")
                    return content
                else:
                    # Fallback to normal pipeline generation
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