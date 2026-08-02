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
        {
            "question": "What is the name of the variable in this code: 'for i in range(10):\n    print(i)'? Answer with only the variable name.",
            "answer": "i"},
        {
            "question": "What is the table name without schema mentioned in this Query: 'SELECT A, B, C FROM dbo.employees'? Answer with only the table name.",
            "answer": "employees"},
        {
            "question": "What is the schema name for the table mentioned in this Query: 'SELECT A, B, C FROM hr.employees'? Answer with only the schema name.",
            "answer": "hr"},
        {
            "question": "How many loops are in this code: 'while True:\n    for i in range(10):\n        for j in range(i): \n            print(i, j)'? Answer with only the number.",
            "answer": "3"},
        {"question": "Calculate: 15 + 27. Answer with only the number.", "answer": "42"},
        {"question": "What is the capital city of Japan? Answer with only the city name.", "answer": "Tokyo"},
        {"question": "What is the next number in this sequence: 2, 4, 6, 8? Answer with only the number.",
         "answer": "10"},
        {
            "question": "Which of the following is a programming language: Mozilla, Terminator, Python, Outlook, Snake, Cloud? Answer with only one word.",
            "answer": "Python"},
        {"question": "Is the Earth flat or round? Answer with only one word: 'flat' or 'round'.", "answer": "round"},
        {
            "question": "What is the length of the list in this code: 'my_list = [1, 2, 3, 4, 5]'? Answer with only the number.",
            "answer": "5"},
        {
            "question": "What is the key associated with the value 'apple' in this dictionary: \"{'fruit': 'apple', 'color': 'red'}\"? Answer with only the key name.",
            "answer": "fruit"},
        {
            "question": "How many columns are being selected in this query: 'SELECT id, name, age, email FROM users'? Answer with only the number.",
            "answer": "4"},
        {
            "question": "What is the name of the function defined in this code: 'def calculate_sum(a, b): return a + b'? Answer with only the function name.",
            "answer": "calculate_sum"},
        {
            "question": "What is the column name used in the WHERE clause of this query: 'SELECT * FROM orders WHERE status = \"shipped\"'? Answer with only the column name.",
            "answer": "status"},
        {
            "question": "What is the boolean value of the expression '5 > 10' in Python? Answer with only 'True' or 'False'.",
            "answer": "False"},
        {
            "question": "What is the key for the age value in this JSON: '{\"name\": \"John\", \"age\": 30}'? Answer with only the key name.",
            "answer": "age"},
        {"question": "What is the result of '10 % 3' in Python? Answer with only the number.", "answer": "1"},
        {
            "question": "What aggregate function is used in this query: 'SELECT COUNT(*) FROM employees'? Answer with only the function name.",
            "answer": "COUNT"},
        {"question": "What is the index of the first element in a Python list? Answer with only the number.",
         "answer": "0"},
        {
            "question": "What is the attribute used to specify the link destination in this code: '<a href=\"https://example.com\">Link</a>'? Answer with only the attribute name.",
            "answer": "href"}
    ]

    prompt_template1 = """You are a strict data-extraction engine. You must output EXACTLY ONE WORD OR NUMBER.
    Do not use punctuation (no periods, no commas). Do not explain. Do not write full sentences.

    Examples:
    Question: What is 2+2? Answer with only the number.
    Output: 4

    Question: What is the capital of France? Answer with only the city name.
    Output: Paris

    Question: {question}
    Output:"""

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

    run_benchmark(client, questions1, prompt_template1, test_models, 12)


def run_benchmark(
        client: TextToTextClient,
        questions: list[dict[str, str]],
        prompt_template: str,
        test_models: list[str | Any],
        limit: int = 99999999):
    # Make list of models distinct
    test_models = list(dict.fromkeys(test_models))

    results = []
    total_start_time = time.time()

    for model_id in test_models[:limit]:
        print(f"\nBenchmarking {model_id}...")
        model_results = {"model_id": model_id, "scores": [], "times": [], "total_time": 0.0}
        for i, q in enumerate(questions):
            start_time = time.time()
            start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"  [{start_timestamp}] Sending request {i + 1}/{len(questions)}...")
            try:
                final_prompt = prompt_template.format(question=q["question"])
                response = client.generate(model_id, final_prompt, model_limit_seconds=60)
                end_time = time.time()
                duration = end_time - start_time
                end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                generated_text = response.get("generated_text", "")
                if not isinstance(generated_text, str):
                    generated_text = str(generated_text)
                print(f"  [{end_timestamp}] Received response in {duration:.2f}s")
                is_correct = (q["answer"].strip().lower() == generated_text.strip().lower())
                model_results["scores"].append("ok" if is_correct else "fail")
                model_results["times"].append(duration)
                model_results["total_time"] += duration
                print(f"  Q: {q['question'][:70]}... -> {'ok' if is_correct else 'fail'}")
                print(f"  A: {generated_text[:len(q["answer"]) * 5]} ({duration:.2f}s)")
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

    print("\n" + "=" * 110)
    print(
        f"{'Model ID':<35} | {'Successes':<10} | {'Failures':<10} | {'Results':<20} | {'Accuracy':<10} | {'Total Time':<10}")
    print("-" * 110)
    for res in results:
        scores_str = " ".join(res["scores"])
        accuracy = sum(1 for s in res["scores"] if s == "ok") / len(res["scores"]) * 100
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

        print(
            f"{res['model_id']:<35} | {init_ok:<10} | {init_fail:<10} | "
            f"{scores_str:<20} | {accuracy:>5.1f}%    | {total_time_str_res:<10}")
    print("=" * 110)
    print(f"Total Benchmark Time: {total_time_str}")