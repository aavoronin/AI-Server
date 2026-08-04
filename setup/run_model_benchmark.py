import time
from datetime import datetime
from typing import Any, Literal
from collections import defaultdict

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

    prompt_template = """You are a strict data-extraction engine. You must output EXACTLY ONE WORD OR NUMBER."""
    prompt_template = "{question} /no_think "



    test_models = [
        # 🥇 Top Picks: Coder Models (Absolute best for strict JSON, zero fluff, highly literal)
        "Qwen/Qwen2.5-Coder-0.5B-Instruct",
        "deepseek-ai/deepseek-coder-1.3b-instruct",
        "Qwen/Qwen2.5-Coder-3B-Instruct",

        # 🥈 Excellent Small Instruct Models (Tiny, robotic, very direct, low VRAM usage)
        "Qwen/Qwen2-0.5B-Instruct",
        "Qwen/Qwen2-1.5B-Instruct",
        "Qwen/Qwen2.5-0.5B-Instruct",
        "Qwen/Qwen2.5-1.5B-Instruct",
        "Qwen/Qwen2.5-3B-Instruct",
        "HuggingFaceTB/SmolLM2-135M-Instruct",
        "unsloth/SmolLM2-135M-Instruct",
        "unsloth/SmolLM-135M-Instruct",
        "unsloth/SmolLM-360M-Instruct",
        "unsloth/SmolLM2-360M-Instruct",
        "unsloth/SmolLM-1.7B-Instruct",
        "unsloth/SmolLM2-1.7B-Instruct",
        "LiquidAI/LFM2.5-1.2B-Instruct",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "allenai/OLMo-2-0425-1B-Instruct",
        "OpenLLM-France/Luciole-1B-Instruct-1.1",
        "tencent/Hunyuan-1.8B-Instruct",

        # 🥉 Strong Mid-Size Instruct Models (Best balance for complex JSON, fit in 12GB VRAM with 4-bit/8-bit)
        "apple/CLaRa-7B-Instruct",
        "microsoft/Phi-4-mini-instruct",
        "unsloth/Llama-3.2-1B-Instruct",
        "unsloth/Llama-3.2-3B-Instruct",
        "unsloth/Phi-3-mini-4k-instruct",
        "microsoft/Phi-3-mini-128k-instruct",
        "microsoft/Phi-3-mini-4k-instruct",
        "Qwen/Qwen2.5-7B-Instruct",

        # ✅ Recommended Quantized Formats (GGUF / GPTQ / BNB-4bit) of the above models
        "TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",
        "TheBlokeAI/Mixtral-tiny-GPTQ",
        "mlx-community/SmolLM3-3B-4bit",
        "unsloth/SmolLM2-135M-Instruct-bnb-4bit",
        "unsloth/SmolLM2-1.7B-Instruct-bnb-4bit",
        "nakue/SmolLM2-1.7B-W4A16-instruct",
        "nm-testing/SmolLM-1.7B-Instruct-quantized.w4a16",
        "Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF",
        "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF"  # Note: 12B Q5 is ~10-11GB, fits tightly in 12GB VRAM
    ]
    print("=== RUNNING FIRST BENCHMARK (Questions 1) ===")
    #results1 = run_benchmark(client, questions1, prompt_template, test_models[:2], 99999999)

    #results1 = run_benchmark(client, questions1, prompt_template,
    #                         test_models, 99999999, cache_models_only=True)
    results1 = run_benchmark(client, questions1, prompt_template,
                             test_models, 99999999,
                             cache_models_only=False,
                             request_timeout=60 * 10)

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
        limit: int = 99999999,
        cache_models_only = False,
        request_timeout = 60):
    # Make list of models distinct
    test_models = list(dict.fromkeys(test_models))

    results = []
    total_start_time = time.time()

    # Save tuples of (question, model, answer)
    answers_list = []

    for model_id in test_models[:limit]:
        print(f"\nBenchmarking {model_id}...")
        model_results = {"model_id": model_id, "scores": [], "times": [], "total_time": 0.0}
        debug_printed = False

        start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{start_timestamp} caching model {model_id}")
        client.cache_model(model_id)
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{end_timestamp} model cached {model_id}")
        if cache_models_only:
            continue

        abort = False
        for i, q in enumerate(questions):
            for k in range(2 if i == 0 else 1):
                debug_printed, abort = make_one_request(
                    answers_list, client, debug_printed,
                    end_timestamp, i, k, model_id,
                    model_results, prompt_template, q, questions,
                    request_timeout)
                if abort:
                    break
            if abort:
                break

        results.append(model_results)
        if i % 5 == 0 and i > 0:
            print_answers(answers_list)

    total_elapsed = time.time() - total_start_time
    m, s = divmod(int(total_elapsed), 60)
    total_time_str = f"{m}:{s:02d}"

    print_answers(answers_list)

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


def make_one_request(
        answers_list: list[Any],
        client: TextToTextClient,
        debug_printed: bool,
        end_timestamp: str,
        i: int | Literal[0],
        k: int,
        model_id: str,
        model_results: dict[str, str | list[Any] | float],
        prompt_template: str,
        q: dict[str, str],
        questions: list[dict[str, str]],
        request_timeout: int):

    abort = False
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{start_timestamp} Sending request {i + 1}/{len(questions)}...")
    try:
        final_prompt = prompt_template.format(question=q["question"])
        if i == 0:
            print(f"prompt: {final_prompt}")
        response = client.generate(model_id, final_prompt, model_limit_seconds=request_timeout)
        print(f"full response: {str(response)[:1024 * 2]}")
        end_time = time.time()
        duration = end_time - start_time
        if k == 0 and i == 0:
            print(f"{end_timestamp} Test run duration {duration:.2f}s")
        else:
            # answers_list.append(q["answer"])
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

            # Save tuple for the new table
            answers_list.append((q["question"], model_id, generated_text.strip()))
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = str(e)
        print(f"  [{end_timestamp}] Request failed after {duration:.2f}s: {error_msg}")
        # Print debug info on client side when error occurs
        if not debug_printed:
            print_model_debug_info(model_id)
            debug_printed = True

        # Save '-' for the new table
        answers_list.append((q["question"], model_id, "-"))

        if i == 0 and "500" in error_msg:
            print(f"  Q: {q['question'][:70]}... -> fail (500 Error on 1st question, aborting model)")
            model_results["scores"].append("fail")
            model_results["times"].append(duration)
            model_results["total_time"] += duration
            # Mark remaining questions as fail with 0 time
            for j in range(i + 1, len(questions)):
                model_results["scores"].append("fail")
                model_results["times"].append(0.0)
                answers_list.append((questions[j]["question"], model_id, "-"))
            abort = True
        else:
            model_results["scores"].append("fail")
            model_results["times"].append(duration)
            model_results["total_time"] += duration
            print(f"  Q: {q['question'][:70]}... -> fail (Error)")
    return debug_printed, abort


def print_answers(answers_list: list[Any]):
    # Print the new table format before the final result
    print("\n" + "=" * 110)
    print("ANSWERS BY QUESTION")
    print("=" * 110)

    # Group by question
    answers_by_question = defaultdict(list)
    for q_text, model_id, answer in answers_list:
        answers_by_question[q_text].append((model_id, answer))

    for q_text, model_answers in answers_by_question.items():
        print(f"\n{q_text}")
        for model_id, answer in model_answers:
            clean_answer = "".join(c for c in answer[:800] if c.isprintable())
            print(f"  {model_id}: {clean_answer[:80]}")
    print("\n" + "=" * 110)