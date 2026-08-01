import json
import subprocess
import sys

from ai_clients.model_client_base import ModelClientBase


def start_wsl_server():
    """Start the AI server inside WSL from Windows."""
    wsl_distro = "Ubuntu"
    wsl_user = "av"
    wsl_workdir = "/home/av/ai-server"
    conda_env = "AI-Server"

    # Kill any existing process on port 8000 to prevent "address already in use"
    kill_cmd = "fuser -k 8000/tcp 2>/dev/null || true"
    start_cmd = f"conda activate {conda_env} && cd {wsl_workdir} && python main.py"

    command = [
        "wsl",
        "-d", wsl_distro,
        "-u", wsl_user,
        "--",
        "bash", "-ic", f"{kill_cmd}; {start_cmd}"
    ]

    print(f"Starting AI server in WSL ({wsl_distro})...")
    print(f"Working directory: {wsl_workdir}")
    print(f"Conda environment: {conda_env}")
    print("Access the server in your browser at: http://localhost:8000 or http://127.0.0.1:8000")

    try:
        subprocess.Popen(command)
        print("Server started in background. Control released.")
    except FileNotFoundError:
        print("WSL is not installed or 'wsl' command not found.")
        sys.exit(1)


def run_caching():
    client = ModelClientBase()
    test_models = [
        "Qwen/Qwen3-0.6B-GGUF",
        "Qwen/Qwen2.5-0.5B-Instruct",
        "LiquidAI/LFM2-1.2B",
        "Qwen/Qwen3-Embedding-0.6B",
        "unsloth/Qwen3-0.6B",
        "Qwen/Qwen3-1.7B-GGUF",

        # Standard Transformers Models (PyTorch/TensorFlow)
        "Qwen/Qwen2.5-0.5B",
        "microsoft/deberta-v3-base",
        "sentence-transformers/all-MiniLM-L6-v2",
        "BAAI/bge-base-en",
        "google-bert/bert-base-cased",

        # GGUF Models (GGML Format)
        "Qwen/Qwen3-0.6B-GGUF",
        "ggml-org/bge-m3-Q8_0-GGUF",
        "lmstudio-community/SmolLM2-135M-Instruct-GGUF",
        "hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF",
        "QuantFactory/SmolLM2-135M-GGUF",

        # GPTQ Models (Quantized)
        "TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",
        "TheBlokeAI/Mixtral-tiny-GPTQ",

        # ONNX Models (Optimized Inference)
        "Qdrant/all-MiniLM-L6-v2-onnx",
        "corto-ai/jina-reranker-v1-turbo-en-onnx",
        "Qdrant/bge-small-en-v1.5-onnx-Q",
        "Qdrant/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q",

        # MLX Models (Apple Silicon)
        "mlx-community/SmolLM3-3B-4bit",
        "mlx-community/starcoder2-3b-4bit",
        "prism-ml/Bonsai-8B-mlx-1bit",
        "prism-ml/Ternary-Bonsai-1.7B-mlx-2bit",

        # BitsAndBytes Quantized (4-bit/8-bit)
        "unsloth/SmolLM2-135M-Instruct-bnb-4bit",
        "unsloth/SmolLM2-360M-bnb-4bit",
        "unsloth/SmolLM2-1.7B-bnb-4bit",
        "unsloth/SmolLM2-1.7B-Instruct-bnb-4bit",
        "unsloth/DeepSeek-R1-Distill-Qwen-1.5B-unsloth-bnb-4bit",

        # AWQ Quantized (Activation-aware Weight Quantization)
        "nakue/SmolLM2-1.7B-W4A16-instruct",
        "nm-testing/SmolLM-1.7B-Instruct-quantized.w4a16",

        # vLLM Optimized (High-Performance Serving)
        "Qwen/Qwen3-0.6B-FP8",
        "Qwen/Qwen2.5-0.5B",
        "microsoft/deberta-v3-base",

        # ExLlamaV2 (Fast Inference)
        "Qwen/Qwen2.5-0.5B",
        "Qwen/Qwen3-0.6B",

        # CTranslate2 (Optimized Inference)
        "Qwen/Qwen2.5-0.5B",
        "microsoft/deberta-v3-base",
    ]
    for test_model_id in test_models:
        print(f"\nTesting cache for {test_model_id}...")
        try:
            cache_result = client.cache_model(test_model_id)
            print("Cache result:", cache_result)
        except Exception as e:
            print(f"Cache/Uncache test failed: {e}")

    print("\nListing cached models...")
    try:
        cached_list = client.list_cached_models()
        print("Cached models:", json.dumps(cached_list, indent=2))
    except Exception as e:
        print(f"Failed to list cached models: {e}")


def stop_wsl_server():
    """Stop the AI server running inside WSL."""
    wsl_distro = "Ubuntu"
    wsl_user = "av"

    command = [
        "wsl",
        "-d", wsl_distro,
        "-u", wsl_user,
        "--",
        "bash", "-c", "fuser -k 8000/tcp 2>/dev/null || true"
    ]

    print("Stopping AI server in WSL...")
    try:
        subprocess.run(command, check=True)
        print("Server stopped successfully.")
    except Exception as e:
        print(f"Failed to stop server: {e}")