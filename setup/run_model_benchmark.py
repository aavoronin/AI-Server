import time
import json
from datetime import datetime
from typing import Any
from collections import defaultdict
from pathlib import Path

from ai_clients.model_client_base import TextToTextClient
from setup.start_server import print_model_debug_info
from setup.questions_helper import QuestionsHelper


def format_time(total_elapsed):
    m, s = divmod(int(total_elapsed), 60)
    return f"{m}:{s:02d}"


def format_value(val):
    return str(val).replace('\n', ' ').replace('"', "'") if val is not None else ""


def compare_values(actual_value, expected_value):
    if isinstance(expected_value, list):
        actual_list = sorted([str(v).strip().lower() for v in actual_value]) if isinstance(actual_value, list) else []
        expected_list = sorted([str(v).strip().lower() for v in expected_value])
        return actual_list == expected_list
    else:
        actual_str = str(actual_value).strip().lower() if actual_value is not None else ""
        expected_str = str(expected_value).strip().lower()
        return actual_str == expected_str


def compare_json_with_expected(expected_json, parsed_dict):
    for key, expected_value in expected_json.items():
        expected_disp = format_value(expected_value)
        if parsed_dict is not None and key in parsed_dict:
            actual_value = parsed_dict[key]
            actual_disp = format_value(actual_value)
            if compare_values(actual_value, expected_value):
                print(f'    "{key}": ok ("{actual_disp}")')
            else:
                print(f'    "{key}": fail ("{actual_disp}"|"{expected_disp}")')
        else:
            print(f'    "{key}": fail (|"{expected_disp}")')


def print_json_failures(expected_json, parsed_dict):
    for key, expected_value in expected_json.items():
        expected_disp = format_value(expected_value)
        if parsed_dict is not None and key in parsed_dict:
            actual_value = parsed_dict[key]
            actual_disp = format_value(actual_value)
            if not compare_values(actual_value, expected_value):
                print(f'    "{key}": fail ("{actual_disp}"|"{expected_disp}")')
        else:
            print(f'    "{key}": fail (|"{expected_disp}")')


def record_failure(model_results, duration, is_json=False, expected_keys=0):
    model_results["scores"].append(0.0 if is_json else "fail")
    model_results["times"].append(duration)
    model_results["total_time"] += duration
    if is_json:
        model_results["total_expected_keys"] += expected_keys


def parse_json_safely(json_output: str) -> Any:
    parsed_dict = None
    try:
        parsed_output = json_output.strip()
        if parsed_output.startswith("```"):
            parsed_output = parsed_output[3:].strip()
            if parsed_output.lower().startswith("json"):
                parsed_output = parsed_output[4:].strip()
            if parsed_output.endswith("```"):
                parsed_output = parsed_output[:-3].strip()
        parsed_dict = json.loads(parsed_output)
    except Exception:
        parsed_dict = None
    return parsed_dict


def evaluate_json_response(output_text: str, expected_json: dict) -> float:
    """Evaluates if the model's output is valid JSON and matches expected keys/values."""
    output_text = output_text.strip()

    if output_text.startswith("```"):
        output_text = output_text[3:].strip()
        if output_text.lower().startswith("json"):
            output_text = output_text[4:].strip()
        if output_text.endswith("```"):
            output_text = output_text[:-3].strip()

    output_text = output_text.strip()

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
            if isinstance(actual_value, list):
                actual_set = set([str(v).strip().lower() for v in actual_value])
            else:
                actual_set = set([str(actual_value).strip().lower()]) if actual_value is not None else set()

            expected_set = set([str(v).strip().lower() for v in expected_value])
            if actual_set == expected_set:
                correct_keys += 1
        else:
            actual_value_str = str(actual_value).strip().lower() if actual_value is not None else ""
            expected_value_str = str(expected_value).strip().lower()
            if actual_value_str == expected_value_str:
                correct_keys += 1

    return correct_keys / total_keys if total_keys > 0 else 0.0


def run_model_benchmark():
    """Benchmark models by asking a series of questions and measuring correctness/time."""
    client = TextToTextClient()
    questions1 = QuestionsHelper.get_questions1()
    questions2 = QuestionsHelper.get_questions2()

    test_models = [
        "Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",
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
                record_failure(model_results, 0.0)
            results.append(model_results)
            continue

        if cache_models_only:
            continue

        for i, q in enumerate(questions):
            start_time = time.time()
            start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"  [{start_timestamp}] Sending request {i + 1}/{len(questions)}...")
            try:
                response = client.generate(model_id, q["question"], model_limit_seconds=60)
                end_time = time.time()
                duration = end_time - start_time
                end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                generated_text = response.get("generated_text", "")
                if not isinstance(generated_text, str):
                    generated_text = str(generated_text)
                print(f"  {end_timestamp} Received response in {duration:.2f}s")
                is_correct = (q["answer"].strip().lower() == generated_text.strip().lower())
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
                if not debug_printed:
                    print_model_debug_info(model_id)
                    debug_printed = True

                record_failure(model_results, duration)

                if i == 0 and "500" in error_msg:
                    print(f"  Q: {q['question'][:70]}... -> fail (500 Error on 1st question, aborting model)")
                    for _ in range(len(questions) - 1):
                        record_failure(model_results, 0.0)
                    break
                else:
                    print(f"  Q: {q['question'][:70]}... -> fail (Error)")
        results.append(model_results)

    total_elapsed = time.time() - total_start_time
    total_time_str = format_time(total_elapsed)

    print("\n" + "=" * 90)
    print(f"{'Model ID':<35} | {'Results':<20} | {'Accuracy':<10} | {'Total Time':<10}")
    print("-" * 90)
    for res in results:
        scores_str = " ".join(res["scores"])
        accuracy = sum(1 for s in res["scores"] if s == "ok") / len(res["scores"]) * 100
        res_time_str = format_time(res["total_time"])
        print(f"{res['model_id']:<35} | {scores_str:<20} | {accuracy:>5.1f}%    | {res_time_str:<10}")
    print("=" * 90)

    return results


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

            try:
                response = client.generate(model_id, q["question"], model_limit_seconds=request_timeout)
                end_time = time.time()
                duration = end_time - start_time
                generated_text = response.get("generated_text", "")
                if not isinstance(generated_text, str):
                    generated_text = str(generated_text)

                score = evaluate_json_response(generated_text, q["expected_json"])

                json_output_one_line = generated_text.replace('\n', ' ').replace('\r', ' ').strip()
                print(f"Time Taken: {duration:.2f}s | Score: {score:.2f}")

                if score < 1.0:
                    parsed_dict = parse_json_safely(json_output_one_line)
                    print_json_failures(q["expected_json"], parsed_dict)

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

                record_failure(model_results, duration, is_json=True, expected_keys=len(q["expected_json"]))

                answers_by_q[i][model_id] = {
                    "time": duration,
                    "score": 0.0,
                    "json_output": f"ERROR: {error_msg}"
                }

                if i == 0 and "500" in error_msg:
                    for j in range(i + 1, len(questions)):
                        record_failure(model_results, 0.0, is_json=True,
                                       expected_keys=len(questions[j]["expected_json"]))
                        answers_by_q[j][model_id] = {"time": 0.0, "score": 0.0, "json_output": "ABORTED"}
                    break

        results.append(model_results)

    total_elapsed = time.time() - total_start_time
    total_time_str = format_time(total_elapsed)

    print("\n" + "=" * 110)
    print("PER-QUESTION SUMMARY")
    print("=" * 110)
    for q_idx, q in enumerate(questions):
        print(f"\n{q['question']}")
        for res in results:
            model_id = res["model_id"]
            data = answers_by_q[q_idx].get(model_id, {"time": 0.0, "score": 0.0, "json_output": "SKIPPED"})
            print(f"  {model_id} ({data['time']:.2f}s): Score: {data['score']:.2f}")

            json_output = data["json_output"]
            expected_json = q["expected_json"]

            parsed_dict = parse_json_safely(json_output)
            compare_json_with_expected(expected_json, parsed_dict)

    print("\n" + "=" * 110)
    print(f"{'Model ID':<50} | {'Total Score':<12} | {'Total Time':<10} | Results Scores")
    print("-" * 110)
    for res in results:
        if res["total_expected_keys"] > 0:
            total_score_pct = (res["total_correct_keys"] / res["total_expected_keys"]) * 100
        else:
            total_score_pct = 0.0

        res_time_str = format_time(res["total_time"])

        scores_str = " ".join(f"{s:.2f}" for s in res["scores"])
        print(f"{res['model_id']:<50} | {total_score_pct:>6.2f}%    | {res_time_str:<10} | {scores_str}")
    print("=" * 110)
    print(f"Total Benchmark Time: {total_time_str}")

    return results

def shorten_vacancy_text(v_name: str, v_text: str) -> str:
    vacancy_slice = [
        ("LinkedIn_Vacancy", "About the job", "Unlock hiring insights"),
        ("Hirify_Vacancy", "Job description", ""),
    ]

    for prefix, start_marker, end_marker in vacancy_slice:
        if v_name.startswith(prefix):
            start_idx = 0
            if start_marker:
                idx = v_text.find(start_marker)
                if idx != -1:
                    start_idx = idx + len(end_marker)

            end_idx = len(v_text)
            if end_marker:
                idx = v_text.rfind(end_marker)
                if idx != -1:
                    end_idx = idx

            return v_text[start_idx:end_idx].strip()
    return v_text


def run_models_on_vacancies(vacancies_dir: str):
    """Benchmark models on real vacancy text files against ground truth JSONs."""
    client = TextToTextClient()
    vacancies_path = Path(vacancies_dir)


    prompt_files = [
        "PROMPT_01.txt",
        "PROMPT_02.txt",
        "PROMPT_03.txt",
        "PROMPT_04.txt",
        "PROMPT_05.txt",
        "PROMPT_06.txt",
        "PROMPT_07.txt"
    ]

    # Find all vacancy txt files and their corresponding result jsons
    vacancies = []
    for txt_file in sorted(vacancies_path.glob("*.txt")):
        result_json_file = txt_file.with_name(txt_file.stem + "_result.json")
        if result_json_file.exists():
            vacancies.append((txt_file, result_json_file))

    if not vacancies:
        print(f"No matching vacancy/result pairs found in {vacancies_dir}")
        return

    test_models = [
        "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q5_K_S-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",
    ]

    print("=== RUNNING VACANCIES BENCHMARK ===")
    print(f"Total Models: {len(test_models)}")
    print(f"Total Vacancies: {len(vacancies)}")

    model_summaries = []

    for model_id in test_models:
        print(f"\n{'=' * 80}")
        print(f"Testing Model: {model_id}")
        print(f"{'=' * 80}")

        total_keys = 0
        total_correct_keys = 0
        total_time = 0.0
        vacancy_scores = []

        for txt_file, result_json_file in vacancies:
            vacancy_name = txt_file.stem
            vacancy_text = txt_file.read_text(encoding='utf-8')
            vacancy_text = shorten_vacancy_text(vacancy_name, vacancy_text)

            try:
                with open(result_json_file, 'r', encoding='utf-8') as f:
                    expected_json = json.load(f)
            except json.JSONDecodeError:
                print(f"\n[{vacancy_name}] ERROR: Invalid JSON in {result_json_file.name}. Scoring as 0.00")
                expected_json = {}
            except Exception as e:
                print(f"\n[{vacancy_name}] ERROR: Failed to read {result_json_file.name}: {e}. Scoring as 0.00")
                expected_json = {}

            combined_parsed_dict = {}
            total_vacancy_time = 0.0

            for p_file in prompt_files:
                prompt_path = vacancies_path.parent / p_file
                if not prompt_path.exists():
                    continue
                prompt_text = prompt_path.read_text(encoding='utf-8')
                full_prompt = prompt_text + "\n" + vacancy_text

                start_time = time.time()
                try:
                    response = client.generate(model_id, full_prompt, model_limit_seconds=60 * 10)
                    duration = time.time() - start_time
                    total_vacancy_time += duration

                    generated_text = response.get("generated_text", "")
                    if not isinstance(generated_text, str):
                        generated_text = str(generated_text)

                    parsed_dict = parse_json_safely(generated_text)
                    if parsed_dict is not None:
                        for key, value in parsed_dict.items():
                            if key not in combined_parsed_dict:
                                combined_parsed_dict[key] = value

                    print(
                        f"  [{p_file}] Time: {duration:.2f}s | Valid JSON: {'Yes' if parsed_dict is not None else 'No'}")

                except Exception as e:
                    duration = time.time() - start_time
                    total_vacancy_time += duration
                    print(f"  [{p_file}] ERROR: {str(e)} | Time: {duration:.2f}s")

            # Evaluate combined result
            keys_in_expected = len(expected_json)
            correct_keys = 0
            if keys_in_expected > 0:
                for key, expected_value in expected_json.items():
                    actual_value = combined_parsed_dict.get(key)
                    if compare_values(actual_value, expected_value):
                        correct_keys += 1

            score = correct_keys / keys_in_expected if keys_in_expected > 0 else 0.0

            total_keys += keys_in_expected
            total_correct_keys += correct_keys

            vacancy_scores.append({
                "vacancy": vacancy_name,
                "score": score,
                "time": total_vacancy_time
            })

            print(f"\n[{vacancy_name}] Combined Time: {total_vacancy_time:.2f}s | Score: {score:.2f}")
            if score < 1.0 and keys_in_expected > 0:
                print_json_failures(expected_json, combined_parsed_dict)
            elif keys_in_expected == 0:
                print(f"  (Skipped failure details due to empty expected JSON)")

        # Model Summary
        avg_score = (total_correct_keys / total_keys) if total_keys > 0 else 0.0
        m, s = divmod(int(total_time), 60)
        time_str = f"{m}:{s:02d}"

        print(f"\n--- Summary for {model_id} ---")
        for vs in vacancy_scores:
            print(f"  {vs['vacancy']:<40} | Score: {vs['score']:.2f} | Time: {vs['time']:.2f}s")
        print(f"  {'AVERAGE':<40} | Score: {avg_score:.2%} | Total Time: {time_str}")

        model_summaries.append({
            "model_id": model_id,
            "avg_score": avg_score,
            "total_time": total_time,
            "time_str": time_str
        })

    # Final Overall Summary
    print("\n" + "=" * 90)
    print(f"{'Model ID':<50} | {'Avg Score':<12} | {'Total Time':<10}")
    print("-" * 90)
    for ms in model_summaries:
        print(f"{ms['model_id']:<50} | {ms['avg_score']:>6.2%}    | {ms['time_str']:<10}")
    print("=" * 90)


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

    for volume in [0.3, 1]:
        questions_slice_index = int(volume * len(questions)) if volume < 1 else len(questions)
        questions_slice_index = 1 if questions_slice_index == 0 else questions_slice_index
        test_models_index = int(volume * len(test_models)) if volume < 1 else len(test_models)
        test_models_index = 1 if test_models_index == 0 else test_models_index
        run_benchmark_json(
            client=client,
            questions=questions[:questions_slice_index],
            test_models=test_models[:test_models_index],
            limit=99999999,
            request_timeout=60 * 10
        )