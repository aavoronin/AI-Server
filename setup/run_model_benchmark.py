import time
import json
from datetime import datetime
from typing import Any
from collections import defaultdict

from ai_clients.model_client_base import TextToTextClient
from setup.start_server import print_model_debug_info
from setup.questions_helper import QuestionsHelper


def run_model_benchmark():
    """Benchmark models by asking a series of questions and measuring correctness/time."""
    client = TextToTextClient()
    questions1 = QuestionsHelper.get_questions1()
    questions2 = QuestionsHelper.get_questions2()

    test_models = [
        "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q5_K_S-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF",
        "NikolayKozloff/Mistral-Nemo-Instruct-2407-Q8_0-GGUF",
        "Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF",
        "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF",
        "unsloth/gemma-3-1b-it-unsloth-bnb-4bit",
        "unsloth/gemma-3-1b-pt-unsloth-bnb-4bit",
        "mlx-community/gemma-3-1b-it-4bit",
        "google/gemma-3n-E4B-it-litert-lm",
        "deepseek-ai/deepseek-coder-7b-instruct-v1.5",
        "Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",
        "lynnea1517/huihui-ai_gemma-3-27b-it-abliterated-Q8_0-GGUF",
        "paultimothymooney/gemma-3-27b-it-Q8_0-GGUF",
        "aminlouhichi/gemma-3-merged-GGUF-Q16",
        "mergekit-community/Qwen3-7B-Instruct",
        "Ygz-08123/Qwen3-7B-Instruct-Q2_K-GGUF",
        "Ygz-08123/Qwen3-7B-Instruct-Q4_K_M-GGUF",
        "goodgooodboy/Qwen3-7B-Instruct-Q4_K_M-GGUF",
        "HuggingFaceTB/SmolLM2-135M-Instruct",
        "unsloth/SmolLM2-135M-Instruct",
        "unsloth/SmolLM2-360M-Instruct",
        "unsloth/SmolLM2-1.7B-Instruct",
        "LiquidAI/LFM2.5-1.2B-Instruct",
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        "OpenLLM-France/Luciole-1B-Instruct-1.1",
        "tencent/Hunyuan-1.8B-Instruct",
        "microsoft/Phi-4-mini-instruct",
        "unsloth/Llama-3.2-3B-Instruct",
        "TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",
        "TheBlokeAI/Mixtral-tiny-GPTQ",
        "mlx-community/SmolLM3-3B-4bit",
        "unsloth/SmolLM2-1.7B-Instruct-bnb-4bit",
        "nakue/SmolLM2-1.7B-W4A16-instruct",
    ]

    for model_slice in [10, 14, 9999999]:
        print("=== CACHING MODELS ===")
        run_benchmark(client, questions1,
                      test_models[:model_slice], 99999999,
                      cache_models_only=True,
                      request_timeout=3600 * 4)

        print("=== RUNNING FIRST BENCHMARK (Questions 1) ===")
        print(f"\n=== ALL MODELS: {len(test_models[:model_slice])} ===")
        for m in test_models[:model_slice]:
            print(f"  - {m}")
        results1 = run_benchmark(client, questions1,
                                 test_models[:model_slice], 99999999,
                                 cache_models_only=False,
                                 request_timeout=60 * 10)

        qualified_models = [
            res["model_id"] for res in results1
            if
            len(res["scores"]) > 0 and (sum(1 for s in res["scores"] if s == "ok") / len(res["scores"]) * 100) >= 50.0
        ]

        print(f"\n=== QUALIFIED MODELS (>= 50% accuracy): {len(qualified_models)} ===")
        for m in qualified_models:
            print(f"  - {m}")

        if qualified_models:
            print("\n=== RUNNING SECOND BENCHMARK (Questions 2) ===")
            results2 = run_benchmark(client, questions2,
                                     qualified_models, 99999999,
                                     cache_models_only=False,
                                     request_timeout=60 * 10)


def run_benchmark(
        client: TextToTextClient,
        questions: list[dict[str, str]],
        test_models: list[str],
        limit: int = 99999999,
        cache_models_only: bool = False,
        request_timeout: int = 60):
    test_models = list(dict.fromkeys(test_models))
    results = []
    total_start_time = time.time()
    answers_list = []

    for model_seq, model_id in enumerate(test_models[:limit]):
        print(f"\nBenchmarking {model_id}...")
        model_results = {"model_id": model_id, "scores": [], "times": [], "total_time": 0.0}
        debug_printed = False

        start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{start_timestamp} caching model {model_id}")
        try:
            client.cache_model(model_id)
            end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{end_timestamp} model cached {model_id}")
        except Exception as e:
            print(f"Failed to cache model {model_id}: {e}")
            for _ in range(len(questions)):
                model_results["scores"].append("fail")
                model_results["times"].append(0.0)
            results.append(model_results)
            continue

        if cache_models_only:
            continue

        abort = False
        for i, q in enumerate(questions):
            for k in range(2 if i == 0 else 1):
                debug_printed, abort = make_one_request(
                    answers_list, client, debug_printed,
                    end_timestamp, i, k, model_id,
                    model_results, q, questions,
                    request_timeout)
                if abort:
                    break
            if abort:
                break

        results.append(model_results)
        if model_seq % 5 == 0 and model_seq > 0:
            print_answers(answers_list)

    total_elapsed = time.time() - total_start_time
    m, s = divmod(int(total_elapsed), 60)
    total_time_str = f"{m}:{s:02d}"

    print_answers(answers_list)

    prepared_results = []
    for res in results:
        scores_str = " ".join(res["scores"])
        accuracy = sum(1 for s in res["scores"] if s == "ok") / len(res["scores"]) * 100 if res["scores"] else 0.0
        m_res, s_res = divmod(int(res["total_time"]), 60)
        total_time_str_res = f"{m_res}:{s_res:02d}"

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

    print("\n" + "=" * 110)
    print(
        f"{'Model ID':<50} | {'Successes':<10} | {'Failures':<10} | {'Results':<20} | {'Accuracy':<10} | {'Total Time':<10}")
    print("-" * 110)
    for prep in prepared_results:
        print(
            f"{prep['model_id']:<50} | {prep['init_ok']:<10} | {prep['init_fail']:<10} | "
            f"{prep['scores_str']:<20} | {prep['accuracy']:>5.1f}%    | {prep['total_time_str_res']:<10}")
    print("=" * 110)
    print(f"Total Benchmark Time: {total_time_str}")

    return results


def make_one_request(
        answers_list: list[Any],
        client: TextToTextClient,
        debug_printed: bool,
        end_timestamp: str,
        i: int,
        k: int,
        model_id: str,
        model_results: dict[str, Any],
        q: dict[str, str],
        questions: list[dict[str, str]],
        request_timeout: int):
    abort = False
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{start_timestamp} Sending request {i + 1}/{len(questions)}...")
    try:
        final_prompt = propose_prompt(model_id, q)
        if i == 0:
            print(f"prompt: {final_prompt}")
        response = client.generate(model_id, final_prompt, model_limit_seconds=request_timeout)
        print(f"full response: {str(response)[:1024 * 2]}")
        end_time = time.time()
        duration = end_time - start_time
        if k == 0 and i == 0:
            print(f"{end_timestamp} Test run duration {duration:.2f}s")
        else:
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

            answers_list.append((q["question"], model_id, generated_text.strip(), duration))
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = str(e)
        print(f"  [{end_timestamp}] Request failed after {duration:.2f}s: {error_msg}")
        if not debug_printed:
            print_model_debug_info(model_id)
            debug_printed = True

        answers_list.append((q["question"], model_id, "-", duration))

        if i == 0 and "500" in error_msg:
            print(f"  Q: {q['question'][:70]}... -> fail (500 Error on 1st question, aborting model)")
            model_results["scores"].append("fail")
            model_results["times"].append(duration)
            model_results["total_time"] += duration
            for j in range(i + 1, len(questions)):
                model_results["scores"].append("fail")
                model_results["times"].append(0.0)
                answers_list.append((questions[j]["question"], model_id, "-", 0.0))
            abort = True
        else:
            model_results["scores"].append("fail")
            model_results["times"].append(duration)
            model_results["total_time"] += duration
            print(f"  Q: {q['question'][:70]}... -> fail (Error)")
    return debug_printed, abort


def propose_prompt(model_id: str, q: dict[str, str]) -> str:
    model_id_lower = model_id.lower()
    question = q["question"]

    if "gemma" in model_id_lower:
        prompt_template = "{question} /no_think"
    elif "qwen" in model_id_lower:
        prompt_template = "{question}\n\nOutput ONLY the exact answer requested. Do not repeat the question, do not add punctuation, and do not provide any explanations."
    elif "deepseek" in model_id_lower:
        prompt_template = "{question}\n\nRespond with EXACTLY the requested value and nothing else. Do not output 'Answer:', do not repeat the question, and do not explain."
    elif any(x in model_id_lower for x in
             ["smollm", "tinyllama", "luciole", "hunyuan", "phi", "llama", "mixtral", "olmo", "lfm"]):
        prompt_template = "{question}\n\nRespond with EXACTLY the requested value (e.g., a single word or number) and absolutely nothing else."
    else:
        prompt_template = "{question}\n\nOutput ONLY the exact answer requested, with no additional text, explanations, or punctuation."

    return prompt_template.format(question=question)


def print_answers(answers_list: list[Any]):
    print("\n" + "=" * 110)
    print("ANSWERS BY QUESTION")
    print("=" * 110)

    answers_by_question = defaultdict(list)
    for q_text, model_id, answer, time_taken in answers_list:
        answers_by_question[q_text].append((model_id, answer, time_taken))

    for q_text, model_answers in answers_by_question.items():
        print(f"\n{q_text}")
        for model_id, answer, time_taken in model_answers:
            clean_answer = "".join(c for c in answer[:800] if c.isprintable())
            print(f"  {model_id} ({time_taken:.2f}s): {clean_answer[:200]}")
    print("\n" + "=" * 110)


def evaluate_json_response(output_text: str, expected_json: dict) -> float:
    """Evaluates if the model's output is valid JSON and matches expected keys/values."""
    output_text = output_text.strip()

    # Remove markdown code blocks if present
    if output_text.startswith("```"):
        output_text = output_text[3:].strip()
        if output_text.lower().startswith("json"):
            output_text = output_text[4:].strip()
        if output_text.endswith("```"):
            output_text = output_text[:-3].strip()

    output_text = output_text.strip()

    # Must be strictly JSON
    if not (output_text.startswith('{') and output_text.endswith('}')):
        return 0.0

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        return 0.0

    if not isinstance(parsed, dict):
        return 0.0

    correct_keys = 0
    total_keys = len(expected_json)
    for key, expected_value in expected_json.items():
        actual_value = parsed.get(key)

        if isinstance(expected_value, list):
            # Normalize both to sorted lists of lowercase strings for comparison
            if isinstance(actual_value, list):
                actual_list = sorted([str(v).strip().lower() for v in actual_value])
            else:
                actual_list = sorted([str(actual_value).strip().lower()]) if actual_value is not None else []

            expected_list = sorted([str(v).strip().lower() for v in expected_value])
            if actual_list == expected_list:
                correct_keys += 1
        else:
            actual_value_str = str(actual_value).strip().lower() if actual_value is not None else ""
            expected_value_str = str(expected_value).strip().lower()
            if actual_value_str == expected_value_str:
                correct_keys += 1

    return correct_keys / total_keys if total_keys > 0 else 0.0


def run_benchmark_json(
        client: TextToTextClient,
        questions: list[dict[str, Any]],
        test_models: list[str],
        limit: int = 99999999,
        request_timeout: int = 60):
    test_models = list(dict.fromkeys(test_models))
    results = []
    total_start_time = time.time()
    answers_by_q = defaultdict(dict)

    for model_seq, model_id in enumerate(test_models[:limit]):
        print(f"\nBenchmarking JSON: {model_id}...")
        model_results = {
            "model_id": model_id,
            "scores": [],
            "times": [],
            "total_time": 0.0,
            "total_correct_keys": 0.0,
            "total_expected_keys": 0
        }
        debug_printed = False

        for i, q in enumerate(questions):
            start_time = time.time()
            start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\n[{start_timestamp}] Question {i + 1} | Model: {model_id}")
            print(f"Question Text: {q['question']}")

            try:
                response = client.generate(model_id, q["question"], model_limit_seconds=request_timeout)
                end_time = time.time()
                duration = end_time - start_time
                generated_text = response.get("generated_text", "")
                if not isinstance(generated_text, str):
                    generated_text = str(generated_text)

                score = evaluate_json_response(generated_text, q["expected_json"])

                json_output_one_line = generated_text.replace('\n', ' ').replace('\r', ' ').strip()
                print(f"Answer (JSON): {json_output_one_line}")
                print(f"Time Taken: {duration:.2f}s | Score: {score:.2f}")

                model_results["scores"].append(score)
                model_results["times"].append(duration)
                model_results["total_time"] += duration
                model_results["total_correct_keys"] += score * len(q["expected_json"])
                model_results["total_expected_keys"] += len(q["expected_json"])

                answers_by_q[i][model_id] = {
                    "time": duration,
                    "score": score,
                    "json_output": json_output_one_line
                }

            except Exception as e:
                end_time = time.time()
                duration = end_time - start_time
                error_msg = str(e)

                print(f"Answer: ERROR - {error_msg}")
                print(f"Time Taken: {duration:.2f}s | Score: 0.00")

                if not debug_printed:
                    print_model_debug_info(model_id)
                    debug_printed = True

                model_results["scores"].append(0.0)
                model_results["times"].append(duration)
                model_results["total_time"] += duration
                model_results["total_expected_keys"] += len(q["expected_json"])

                answers_by_q[i][model_id] = {
                    "time": duration,
                    "score": 0.0,
                    "json_output": f"ERROR: {error_msg}"
                }

                if i == 0 and "500" in error_msg:
                    for j in range(i + 1, len(questions)):
                        model_results["scores"].append(0.0)
                        model_results["times"].append(0.0)
                        model_results["total_expected_keys"] += len(questions[j]["expected_json"])
                        answers_by_q[j][model_id] = {"time": 0.0, "score": 0.0, "json_output": "ABORTED"}
                    break

        results.append(model_results)

    total_elapsed = time.time() - total_start_time
    m, s = divmod(int(total_elapsed), 60)
    total_time_str = f"{m}:{s:02d}"

    print("\n" + "=" * 110)
    print("PER-QUESTION SUMMARY")
    print("=" * 110)
    for q_idx, q in enumerate(questions):
        print(f"\nQuestion {q_idx + 1}: {q['summary']}")
        for res in results:
            model_id = res["model_id"]
            data = answers_by_q[q_idx].get(model_id, {"time": 0.0, "score": 0.0, "json_output": "SKIPPED"})
            print(f"  {model_id} ({data['time']:.2f}s): Score: {data['score']:.2f} | {data['json_output'][:100]}")

    print("\n" + "=" * 110)
    print(f"{'Model ID':<50} | {'Results (First 10)':<30} | {'Total Score':<12} | {'Total Time':<10}")
    print("-" * 110)
    for res in results:
        if res["total_expected_keys"] > 0:
            total_score_pct = (res["total_correct_keys"] / res["total_expected_keys"]) * 100
        else:
            total_score_pct = 0.0

        m_res, s_res = divmod(int(res["total_time"]), 60)
        total_time_str_res = f"{m_res}:{s_res:02d}"

        scores_str = " ".join(f"{s:.2f}" for s in res["scores"][:10])
        if len(res["scores"]) > 10:
            scores_str += " ..."

        print(f"{res['model_id']:<50} | {scores_str:<30} | {total_score_pct:>6.2f}%    | {total_time_str_res:<10}")
    print("=" * 110)
    print(f"Total Benchmark Time: {total_time_str}")

    return results


def run_model_benchmark_json():
    """Benchmark models on JSON extraction from vacancy texts."""
    client = TextToTextClient()
    questions = QuestionsHelper.get_vacancy_json_questions()

    test_models = [
        "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q5_K_S-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF",
        "Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF",
        "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF",
    ]

    print("=== RUNNING JSON BENCHMARK ===")
    print(f"Total Models: {len(test_models)}")
    print(f"Total Questions: {len(questions)}")

    run_benchmark_json(
        client=client,
        questions=questions,
        test_models=test_models,
        limit=99999999,
        request_timeout=60 * 10
    )