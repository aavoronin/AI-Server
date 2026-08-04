test_models0 = [
        # 🥈 Excellent Small Instruct Models (Tiny, robotic, very direct)
        "Qwen/Qwen2-0.5B-Instruct",  # Instruct
        "Qwen/Qwen2-1.5B-Instruct",  # Instruct
        "HuggingFaceTB/SmolLM2-135M-Instruct",  # Instruct
        "unsloth/SmolLM2-135M-Instruct",  # Instruct
        "unsloth/SmolLM-135M-Instruct",  # Instruct
        "unsloth/SmolLM-360M-Instruct",  # Instruct
        "unsloth/SmolLM2-1.7B-Instruct",  # Instruct
        "LiquidAI/LFM2.5-1.2B-Instruct",  # Instruct
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Chat

        "Alibaba-NLP/gte-base-en-v1.5",
        "LiquidAI/LFM2-1.2B",
        "LiquidAI/LFM2.5-230M",
        "LiquidAI/LFM2.5-230M-Base",
        "LiquidAI/LFM2.5-350M",

        # 🥇 Top Picks: Coder & Math models (Highly literal, rule-following, zero fluff)
        # "01-ai/Yi-Coder-1.5B-Chat",  # Chat
        "01-ai/Yi-Coder-1.5B",
        "Qwen/Qwen2.5-Coder-0.5B-Instruct",  # Instruct
        "Qwen/Qwen2.5-Math-1.5B-Instruct",  # Instruct

        # 🥉 Other Notable Small Instruct Models
        "allenai/OLMo-2-0425-1B-Instruct",  # Instruct
        "OpenLLM-France/Luciole-1B-Instruct-1.1",  # Instruct
        "tencent/Hunyuan-1.8B-Instruct",  # Instruct

        # Base & Unquantized Models
        "Qwen/Qwen1.5-0.5B",
        "Qwen/Qwen2-1.5B",
        "Qwen/Qwen2.5-0.5B",
        "Qwen/Qwen2.5-1.5B",
        "Qwen/Qwen2.5-Coder-1.5B",
        "Qwen/Qwen2.5-Math-1.5B",
        "Qwen/Qwen3-0.6B",
        "Qwen/Qwen3-1.7B",
        "Qwen/Qwen3-1.7B-Base",

        # GGUF Models
        # "Qwen/Qwen3-0.6B-GGUF",  # GGUF
        # "Qwen/Qwen3-1.7B-GGUF",  # GGUF
        # "QuantFactory/SmolLM-135M-GGUF",  # GGUF
        # "QuantFactory/SmolLM-135M-Instruct-GGUF",  # GGUF & Instruct
        # "unsloth/bge-small-en-v1.5-GGUF",  # GGUF

        # Other Models
        "apple/CLaRa-7B-Instruct",  # Instruct
        "deepseek-ai/deepseek-coder-1.3b-instruct",  # Instruct
        "microsoft/Phi-4-mini-instruct",  # Instruct
        "Qwen/Qwen2.5-1.5B-Instruct",  # Instruct
        "Qwen/Qwen2.5-3B-Instruct",  # Instruct
        "Qwen/Qwen2.5-Coder-3B-Instruct",  # Instruct
        "unsloth/Llama-3.2-1B-Instruct",  # Instruct
        "unsloth/Llama-3.2-3B-Instruct",  # Instruct
        "unsloth/Phi-3-mini-4k-instruct",  # Instruct
        "unsloth/SmolLM-1.7B-Instruct",  # Instruct
        "unsloth/SmolLM2-360M-Instruct",  # Instruct

        # (Removed duplicates: "Qwen/Qwen3-0.6B-GGUF", "Qwen/Qwen3-1.7B-GGUF", "Qwen/Qwen2.5-0.5B")
        "Qwen/Qwen2.5-0.5B-Instruct",  # Instruct
        # "LiquidAI/LFM2-1.2B",
        "Qwen/Qwen3-Embedding-0.6B",
        "unsloth/Qwen3-0.6B",
        "unsloth/Qwen3-4B",

        # Embeddings & BERT
        "microsoft/deberta-v3-base",
        "sentence-transformers/all-MiniLM-L6-v2",
        "BAAI/bge-base-en",
        "google-bert/bert-base-cased",

        # GGUF Models
        # "ggml-org/bge-m3-Q8_0-GGUF",  # GGUF
        # "lmstudio-community/SmolLM2-135M-Instruct-GGUF",  # GGUF & Instruct
        # "hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF",  # GGUF & Instruct
        # "QuantFactory/SmolLM2-135M-GGUF",  # GGUF

        # GPTQ Models
        "TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",  # GPTQ & Chat
        "TheBlokeAI/Mixtral-tiny-GPTQ",  # GPTQ

        # ONNX Models
        "Qdrant/all-MiniLM-L6-v2-onnx",
        "corto-ai/jina-reranker-v1-turbo-en-onnx",
        "Qdrant/bge-small-en-v1.5-onnx-Q",
        "Qdrant/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q",

        # MLX Models
        "mlx-community/SmolLM3-3B-4bit",
        "mlx-community/starcoder2-3b-4bit",
        "prism-ml/Bonsai-8B-mlx-1bit",
        "prism-ml/Ternary-Bonsai-1.7B-mlx-2bit",

        # BNB-4bit & Quantized
        "unsloth/SmolLM2-135M-Instruct-bnb-4bit",  # Instruct
        "unsloth/SmolLM2-360M-bnb-4bit",
        "unsloth/SmolLM2-1.7B-bnb-4bit",
        "unsloth/SmolLM2-1.7B-Instruct-bnb-4bit",  # Instruct
        "unsloth/DeepSeek-R1-Distill-Qwen-1.5B-unsloth-bnb-4bit",
        "unsloth/DeepSeek-R1-Distill-Qwen-1.5B",
        "nakue/SmolLM2-1.7B-W4A16-instruct",  # Instruct
        "nm-testing/SmolLM-1.7B-Instruct-quantized.w4a16",  # Instruct

        "Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF",
        "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF",
        "Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",

        "microsoft/phi-2",
        "microsoft/phi-4",
        "microsoft/Phi-3-mini-128k-instruct",
        "microsoft/Phi-3-mini-4k-instruct",

        "Qwen/Qwen2.5-7B",
        "Qwen/Qwen2.5-7B-Instruct",
        "Qwen/Qwen3-8B",
        "Qwen/Qwen3-8B-Base",

        # FP8
        # "Qwen/Qwen3-0.6B-FP8",
    ]