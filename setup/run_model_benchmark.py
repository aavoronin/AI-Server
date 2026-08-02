import time
from datetime import datetime
from typing import Any

from ai_clients.model_client_base import TextToTextClient
from setup.start_server import print_model_debug_info


def run_model_benchmark():
    """Benchmark models by asking a series of questions and measuring correctness/time."""
    client = TextToTextClient()
    questions1 = [
        {"question": "Calculate: 15 + 27. Answer with only the number.", "answer": "42"},
        {"question": "What is the capital city of Japan? Answer with only the city name.", "answer": "Tokyo"},
        {"question": "What is the next number in this sequence: 2, 4, 6, 8? Answer with only the number.",
         "answer": "10"},
        {
            "question": "Which of the following is programming language Mozilla, Terminator, Python, Outlook, Snake, Cloud? Answer with only one word.",
            "answer": "Python"},
        {"question": "Is the Earth flat or round? Answer with only one word: 'flat' or 'round'.", "answer": "round"}
    ]

    questions2 = [
        {"question": "Calculate: 123 * 45. Answer with only the number.", "answer": "5535"},
        {"question": "What is the capital city of Australia? Answer with only the city name.", "answer": "Canberra"},
        {"question": "What is the next number in this sequence: 1, 1, 2, 3, 5? Answer with only the number.",
         "answer": "8"},
        {
            "question": "Which of the following is a database system: Mozilla, PostgreSQL, Terminator, Outlook? Answer with only one word.",
            "answer": "PostgreSQL"},
        {"question": "Is water a solid, liquid, or gas at room temperature? Answer with only one word.",
         "answer": "liquid"}
    ]

    prompt_template = """You are a strict data-extraction engine. You must output EXACTLY ONE WORD OR NUMBER.
Do not use punctuation (no periods, no commas). Do not explain. Do not write full sentences.

Examples:
Question: What is 2+2? Answer with only the number.
Output: 4

Question: What is the capital of France? Answer with only the city name.
Output: Paris

Question: {question}
Output:"""

    test_models = [
        "Alibaba-NLP/gte-base-en-v1.5",
        "LiquidAI/LFM2-1.2B",
        "LiquidAI/LFM2.5-230M",
        "LiquidAI/LFM2.5-230M-Base",
        "LiquidAI/LFM2.5-350M",

        # 🥇 Top Picks: Coder & Math models (Highly literal, rule-following, zero fluff)
        #"01-ai/Yi-Coder-1.5B-Chat",  # Chat
        "01-ai/Yi-Coder-1.5B",
        "Qwen/Qwen2.5-Coder-0.5B-Instruct",  # Instruct
        "Qwen/Qwen2.5-Math-1.5B-Instruct",  # Instruct

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
        #"Qwen/Qwen3-0.6B-GGUF",  # GGUF
        #"Qwen/Qwen3-1.7B-GGUF",  # GGUF
        #"QuantFactory/SmolLM-135M-GGUF",  # GGUF
        #"QuantFactory/SmolLM-135M-Instruct-GGUF",  # GGUF & Instruct
        #"unsloth/bge-small-en-v1.5-GGUF",  # GGUF

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
        #"LiquidAI/LFM2-1.2B",
        "Qwen/Qwen3-Embedding-0.6B",
        "unsloth/Qwen3-0.6B",

        # Embeddings & BERT
        "microsoft/deberta-v3-base",
        "sentence-transformers/all-MiniLM-L6-v2",
        "BAAI/bge-base-en",
        "google-bert/bert-base-cased",

        # GGUF Models
        #"ggml-org/bge-m3-Q8_0-GGUF",  # GGUF
        #"lmstudio-community/SmolLM2-135M-Instruct-GGUF",  # GGUF & Instruct
        #"hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF",  # GGUF & Instruct
        #"QuantFactory/SmolLM2-135M-GGUF",  # GGUF

        # GPTQ Models
        #"TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",  # GPTQ & Chat
        #"TheBlokeAI/Mixtral-tiny-GPTQ",  # GPTQ

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
        "nakue/SmolLM2-1.7B-W4A16-instruct",  # Instruct
        "nm-testing/SmolLM-1.7B-Instruct-quantized.w4a16",  # Instruct

        # FP8
        #"Qwen/Qwen3-0.6B-FP8",
    ]
    print("=== RUNNING FIRST BENCHMARK (Questions 1) ===")
    results1 = run_benchmark(client, questions1, prompt_template, test_models, 99999999)

    qualified_models = [
        res["model_id"] for res in results1
        if len(res["scores"]) > 0 and (sum(1 for s in res["scores"] if s == "ok") / len(res["scores"]) * 100) >= 50.0
    ]

    print(f"\n=== QUALIFIED MODELS (>= 50% accuracy): {len(qualified_models)} ===")
    for m in qualified_models:
        print(f"  - {m}")

    if qualified_models:
        print("\n=== RUNNING SECOND BENCHMARK (Questions 2) ===")
        results2 = run_benchmark(client, questions2, prompt_template, qualified_models, 99999999)
        return results1, results2

    return results1


def run_benchmark(
        client: TextToTextClient,
        questions: list[dict[str, str]],
        prompt_template: str,
        test_models: list[str],
        limit: int = 99999999):
    # Make list of models distinct
    test_models = list(dict.fromkeys(test_models))

    results = []
    total_start_time = time.time()

    for model_id in test_models[:limit]:
        print(f"\nBenchmarking {model_id}...")
        model_results = {"model_id": model_id, "scores": [], "times": [], "total_time": 0.0}
        for i, q in enumerate(questions):
            start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{start_timestamp} caching model")
            client.cache_model(model_id)
            start_time = time.time()
            start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{start_timestamp} Sending request {i + 1}/{len(questions)}...")
            try:
                final_prompt = prompt_template.format(question=q["question"])
                response = client.generate(model_id, final_prompt, model_limit_seconds=60)
                end_time = time.time()
                duration = end_time - start_time
                end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                generated_text = response.get("generated_text", "")
                if not isinstance(generated_text, str):
                    generated_text = str(generated_text)
                print(f"{end_timestamp} Received response in {duration:.2f}s")
                is_correct = (q["answer"].strip().lower() == generated_text.strip().lower())
                model_results["scores"].append("ok" if is_correct else "fail")
                model_results["times"].append(duration)
                model_results["total_time"] += duration
                print(f"  Q: {q['question'][:70]}... -> {'ok' if is_correct else 'fail'}")
                print(f"  A: {generated_text[:len(q['answer']) * 5]} ({duration:.2f}s)")
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

    total_elapsed = time.time() - total_start_time
    m, s = divmod(int(total_elapsed), 60)
    total_time_str = f"{m}:{s:02d}"

    # First loop: collect all final values into prepared_results
    prepared_results = []
    for res in results:
        scores_str = " ".join(res["scores"])
        accuracy = sum(1 for s in res["scores"] if s == "ok") / len(res["scores"]) * 100 if res["scores"] else 0.0
        m_res, s_res = divmod(int(res["total_time"]), 60)
        total_time_str_res = f"{m_res}:{s_res:02d}"

        # Fetch stats
        try:
            stats = client.get_model_stats(res["model_id"])
            init_ok = stats.get("num_init_successes", 0)
            init_fail = stats.get("num_fails", 0)
        except Exception:
            init_ok = 0
            init_fail = 0

        prepared_results.append({
            "model_id": res["model_id"],
            "init_ok": init_ok,
            "init_fail": init_fail,
            "scores_str": scores_str,
            "accuracy": accuracy,
            "total_time_str_res": total_time_str_res
        })

    # Second loop: print table using prepared values
    print("\n" + "=" * 110)
    print(
        f"{'Model ID':<35} | {'Successes':<10} | {'Failures':<10} | {'Results':<20} | {'Accuracy':<10} | {'Total Time':<10}")
    print("-" * 110)
    for prep in prepared_results:
        print(
            f"{prep['model_id']:<35} | {prep['init_ok']:<10} | {prep['init_fail']:<10} | "
            f"{prep['scores_str']:<20} | {prep['accuracy']:>5.1f}%    | {prep['total_time_str_res']:<10}")
    print("=" * 110)
    print(f"Total Benchmark Time: {total_time_str}")

    return results