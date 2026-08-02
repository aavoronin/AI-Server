import time
from datetime import datetime

from ai_clients.model_client_base import TextToTextClient
from setup.start_server import print_model_debug_info


def run_model_benchmark():
    """Benchmark models by asking a series of questions and measuring correctness/time."""
    client = TextToTextClient()
    questions = [
        {"question": "Calculate: 15 + 27. Answer with only the number.", "answer": "42"},
        {"question": "What is the capital city of Japan? Answer with only the city name.", "answer": "Tokyo"},
        {"question": "What is the next number in this sequence: 2, 4, 6, 8? Answer with only the number.",
         "answer": "10"},
        #{"question": "Translate the English word 'apple' to Spanish. Answer with only the translated word.",
        # "answer": "manzana"},
        {"question": "Which of the following is programming language Mozilla, Terminator, Python, Outlook, Snake, Cloud? Answer with only one word.", "answer": "Python"},
        {"question": "Is the Earth flat or round? Answer with only one word: 'flat' or 'round'.", "answer": "round"}
    ]

    test_models = [
        "Qwen/Qwen3-0.6B-GGUF",
        "Qwen/Qwen3-1.7B-GGUF",
        "QuantFactory/SmolLM-135M-GGUF",
        "QuantFactory/SmolLM-135M-Instruct-GGUF",
        "unsloth/bge-small-en-v1.5-GGUF",
        "apple/CLaRa-7B-Instruct",
        "deepseek-ai/deepseek-coder-1.3b-instruct",
        "microsoft/Phi-4-mini-instruct",
        "Qwen/Qwen2.5-1.5B-Instruct",
        "Qwen/Qwen2.5-3B-Instruct",
        "Qwen/Qwen2.5-Coder-3B-Instruct",
        "unsloth/Llama-3.2-1B-Instruct",
        "unsloth/Llama-3.2-3B-Instruct",
        "unsloth/Phi-3-mini-4k-instruct",
        "unsloth/SmolLM-1.7B-Instruct",
        "unsloth/SmolLM2-360M-Instruct",

        "Qwen/Qwen3-0.6B-GGUF",
        "Qwen/Qwen2.5-0.5B-Instruct",
        "LiquidAI/LFM2-1.2B",
        "Qwen/Qwen3-Embedding-0.6B",
        "unsloth/Qwen3-0.6B",
        "Qwen/Qwen3-1.7B-GGUF",
        "Qwen/Qwen2.5-0.5B",
        "microsoft/deberta-v3-base",
        "sentence-transformers/all-MiniLM-L6-v2",
        "BAAI/bge-base-en",
        "google-bert/bert-base-cased",
        "ggml-org/bge-m3-Q8_0-GGUF",
        "lmstudio-community/SmolLM2-135M-Instruct-GGUF",
        "hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF",
        "QuantFactory/SmolLM2-135M-GGUF",
        "TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",
        "TheBlokeAI/Mixtral-tiny-GPTQ",
        "Qdrant/all-MiniLM-L6-v2-onnx",
        "corto-ai/jina-reranker-v1-turbo-en-onnx",
        "Qdrant/bge-small-en-v1.5-onnx-Q",
        "Qdrant/paraphrase-multilingual-MiniLM-L12-v2-onnx-Q",
        "mlx-community/SmolLM3-3B-4bit",
        "mlx-community/starcoder2-3b-4bit",
        "prism-ml/Bonsai-8B-mlx-1bit",
        "prism-ml/Ternary-Bonsai-1.7B-mlx-2bit",
        "unsloth/SmolLM2-135M-Instruct-bnb-4bit",
        "unsloth/SmolLM2-360M-bnb-4bit",
        "unsloth/SmolLM2-1.7B-bnb-4bit",
        "unsloth/SmolLM2-1.7B-Instruct-bnb-4bit",
        "unsloth/DeepSeek-R1-Distill-Qwen-1.5B-unsloth-bnb-4bit",
        "nakue/SmolLM2-1.7B-W4A16-instruct",
        "nm-testing/SmolLM-1.7B-Instruct-quantized.w4a16",
        "Qwen/Qwen3-0.6B-FP8",
    ]

    results = []

    for model_id in test_models[:20]:
        print(f"\nBenchmarking {model_id}...")
        model_results = {"model_id": model_id, "scores": [], "times": [], "total_time": 0.0}

        for i, q in enumerate(questions):
            start_time = time.time()
            start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"  [{start_timestamp}] Sending request {i + 1}/{len(questions)}...")

            try:
                response = client.generate(model_id, q["question"], model_limit_seconds=300)
                end_time = time.time()
                duration = end_time - start_time
                end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                generated_text = response.get("generated_text", "")
                if not isinstance(generated_text, str):
                    generated_text = str(generated_text)

                print(f"  [{end_timestamp}] Received response in {duration:.2f}s")

                is_correct = (q["answer"].strip().lower() in generated_text.strip().lower())
                model_results["scores"].append("ok" if is_correct else "fail")
                model_results["times"].append(duration)
                model_results["total_time"] += duration

                print(f"  Q: {q['question'][:70]}... -> {'ok' if is_correct else 'fail'} ({duration:.2f}s)")

            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_msg = str(e)

                print(f"  [{end_timestamp}] Request failed after {duration:.2f}s: {error_msg}")

                # Print debug info on client side when error occurs
                print_model_debug_info(model_id)

                if i == 0 and "500" in error_msg:
                    print(f"  Q: {q['question'][:70]}... -> fail (500 Error on 1st question, aborting model)")
                    model_results["scores"].append("fail")
                    model_results["times"].append(duration)
                    model_results["total_time"] += duration

                    # Mark remaining questions as fail with 0 time
                    for _ in range(len(questions) - 1):
                        model_results["scores"].append("fail")
                        model_results["times"].append(0.0)
                    break
                else:
                    model_results["scores"].append("fail")
                    model_results["times"].append(duration)
                    model_results["total_time"] += duration
                    print(f"  Q: {q['question'][:70]}... -> fail (Error)")

        results.append(model_results)

    print("\n" + "=" * 90)
    print(f"{'Model ID':<35} | {'Results':<20} | {'Accuracy':<10} | {'Total Time':<10}")
    print("-" * 90)
    for res in results:
        scores_str = " ".join(res["scores"])
        accuracy = sum(1 for s in res["scores"] if s == "ok") / len(res["scores"]) * 100
        m, s = divmod(int(res["total_time"]), 60)
        total_time_str = f"{m}:{s:02d}"
        print(f"{res['model_id']:<35} | {scores_str:<20} | {accuracy:>5.1f}%    | {total_time_str:<10}")
    print("=" * 90)
