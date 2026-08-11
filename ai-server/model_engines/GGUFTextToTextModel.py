from .TextToTextModel import TextToTextModel
import logging

logger = logging.getLogger(__name__)


class GGUFTextToTextModel(TextToTextModel):
    def __init__(self, model_id: str, cache_dir: str):
        super().__init__(model_id, cache_dir)
        self.model = None
        self.tokenizer = None
        self.llm = None
        self.use_llama_cpp = False

    def load(self):
        # 1. Try using llama-cpp-python first (Recommended for GGUF)
        try:
            from llama_cpp import Llama
            logger.info(f"Loading GGUF model with llama-cpp-python: {self.model_id}")
            gguf_files = list(self.model_path.glob("*.gguf"))
            if not gguf_files:
                raise FileNotFoundError(f"No .gguf file found in {self.model_path}")

            gguf_path = str(gguf_files[0])

            # Determine n_ctx based on model size for Gemma-3
            model_id_lower = self.model_id.lower()
            if "gemma-3-1b" in model_id_lower or "gemma-3-1b-it" in model_id_lower:
                n_ctx = 32768  # 32K tokens for 1B size
            else:
                n_ctx = 131072  # 128K tokens for 4B, 12B, and 27B sizes

            # Set verbose=True to see the exact number of layers offloaded to the GPU in the console logs
            self.llm = Llama(
                model_path=gguf_path,
                n_gpu_layers=-1,  # Attempt to offload all layers to GPU
                n_ctx=n_ctx,
                verbose=True
            )
            self.use_llama_cpp = True
            self.is_loaded = True
            logger.info(f"Successfully loaded GGUF {self.model_id} with llama-cpp-python")
            return
        except ImportError:
            logger.info("llama-cpp-python not found, falling back to transformers")
        except Exception as e:
            logger.warning(f"Failed to load with llama-cpp-python: {e}. Falling back to transformers.")

        # 2. Fallback to transformers
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            logger.info(f"Loading GGUF model with Transformers: {self.model_id}")
            gguf_files = list(self.model_path.glob("*.gguf"))
            if not gguf_files:
                raise FileNotFoundError(f"No .gguf file found in {self.model_path}")

            gguf_file = gguf_files[0].name
            logger.info(f"Found GGUF file: {gguf_file}")

            # Try loading tokenizer from the original model ID first
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_id, trust_remote_code=True
                )
            except Exception:
                # If that fails, try the local path
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.model_path, trust_remote_code=True
                    )
                except Exception:
                    # Fallback for known GGUF repos that lack tokenizer files locally
                    model_id_lower = self.model_id.lower()
                    if "gemma-4-e4b" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-4-E4B-it", trust_remote_code=True)
                    elif "gemma-3-4b" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-4b-it", trust_remote_code=True)
                    elif "gemma-3-12b" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-12b-it", trust_remote_code=True)
                    elif "gemma-3-1b" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-1b-it", trust_remote_code=True)
                    elif "qwen3-0.6b" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-0.6B", trust_remote_code=True)
                    elif "qwen3-1.7b" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-1.7B", trust_remote_code=True)
                    elif "smollm-135m-instruct" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M-Instruct",
                                                                       trust_remote_code=True)
                    elif "smollm-135m" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM2-135M",
                                                                       trust_remote_code=True)
                    elif "bge-small-en-v1.5" in model_id_lower:
                        self.tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-en-v1.5", trust_remote_code=True)
                    else:
                        raise

            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                gguf_file=gguf_file,
                torch_dtype="auto",
                device_map="auto",
                trust_remote_code=True
            )
            self.use_llama_cpp = False
            self.is_loaded = True
            logger.info(f"Successfully loaded GGUF {self.model_id} with Transformers")
        except ImportError as e:
            logger.error(f"Failed to load GGUF model {self.model_id}: {e}")
            logger.error("Please install the 'gguf' package: pip install 'gguf>=0.10.0'")
            raise
        except Exception as e:
            logger.error(f"Failed to load GGUF model {self.model_id}: {e}")
            raise

    def unload(self):
        if self.use_llama_cpp:
            if self.llm is not None:
                del self.llm
        else:
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

        # Set max_new_tokens to 8192 for Gemma-3 models as per specification
        model_id_lower = self.model_id.lower()
        default_max_tokens = 8192 if "gemma-3" in model_id_lower else 2048
        max_new_tokens = kwargs.get("max_new_tokens", default_max_tokens)
        temperature = kwargs.get("temperature", 0.7)

        try:
            if self.use_llama_cpp:
                messages = [{"role": "user", "content": prompt}]
                output = self.llm.create_chat_completion(
                    messages=messages,
                    max_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=0.9,
                    stream=False
                )
                return output["choices"][0]["message"]["content"].strip()
            else:
                messages = [{"role": "user", "content": prompt}]
                text = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                model_inputs = self.tokenizer(
                    [text], return_tensors="pt"
                ).to(self.model.device)

                generated_ids = self.model.generate(
                    **model_inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True
                )
                output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
                content = self.tokenizer.decode(
                    output_ids, skip_special_tokens=True
                ).strip("\n")
                return content
        except Exception as e:
            logger.error(f"Generation failed for GGUF {self.model_id}: {e}")
            raise