import time
import json
from datetime import datetime
from typing import Any
from collections import defaultdict

from ai_clients.TextToTextClient import TextToTextClient
from setup.start_server import print_model_debug_info
from setup.questions_helper import QuestionsHelper
from setup.running_model_utils import (
    format_time, record_failure, evaluate_json_response,
    parse_json_safely, print_json_failures, compare_json_with_expected
)


def run_model_benchmark():
    """Benchmark models by asking a series of questions and measuring correctness/time."""
    client = TextToTextClient()
    questions1 = QuestionsHelper.get_questions1()
    questions2 = QuestionsHelper.get_questions2()

    test_models = [
        "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF",
        "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF|GPU|131072",
        "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF|GPU|131072",
        #"google/gemma-4-12B-it-qat-q4_0-unquantized-assistant|GPU|32768",
        "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q4_K_M|GPU|32768",
        "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|32768",
        "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|GPU|32768",
        "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|GPU|32768",
        "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|65536",
        "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|GPU|65536",
        "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|GPU|65536",
        "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|98304",
        "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|GPU|98304",
        "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|GPU|98304",
        #"majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|131072",
        #"majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|GPU|131072",
        #"majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|GPU|131072",

        "soob3123/GrayLine-Gemma3-12B-Q4_K_M-GGUF|GPU|32768",
        "Medvedko/gemma-3-12b-it-heretic-v2-Q4_K_M-GGUF|GPU|32768",
        "ilya-chak/gemma-4-12B-it-qat-GGUF-UD-Q4_K_XL-layers|GPU|32768",
        "nocturne23/gemma-3-12b-it-Q4_K_M-GGUF|GPU|32768",

        "NikolayKozloff/amoral-gemma3-12B-Q5_K_M-GGUF|GPU|32768",
        "NikolayKozloff/amoral-gemma3-12B-Q5_K_M-GGUF|GPU|32768",
        "NikolayKozloff/amoral-gemma3-12B-Q6_K-GGUF|GPU|32768",
        "WesPro/amoral-gemma3-12B-Q6_K-GGUF|GPU|32768",
        "tg-rising/gemma-3-12b-it-heretic-v2-MLX-Q6|GPU|32768",
        "Fazmin/solus_v1_gemma-4-12b-uncensored-q4|GPU|32768",
        "Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF|GPU|32768",
        #"sjoe1244/gemma-4-12B-it-abliterated-uncensored-exl3-4bpw|GPU|32768",
        "Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF|GPU|32768",
        "Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q5_K_S-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF",
        "aminlouhichi/gemma-3-merged-GGUF-Q16",
        "NikolayKozloff/gemma-3-12b-it-Q8_0-GGUF",
        "mlx-community/Huihui-gemma-3n-E4B-it-abliterated-lm-8bit",
        "aryamannningombam/gemma-GPTQ_g128-3bits",
        "bartowski/google_gemma-3n-E4B-it-GGUF",

        # 27B
        #"Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",
        #"Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",
        #"lynnea1517/huihui-ai_gemma-3-27b-it-abliterated-Q8_0-GGUF",
        #"paultimothymooney/gemma-3-27b-it-Q8_0-GGUF",

        #"NikolayKozloff/Mistral-Nemo-Instruct-2407-Q8_0-GGUF",
        #"unsloth/gemma-3-1b-it-unsloth-bnb-4bit",
        #"unsloth/gemma-3-1b-pt-unsloth-bnb-4bit",
        #"mlx-community/gemma-3-1b-it-4bit",
        #"google/gemma-3n-E4B-it-litert-lm",
        #"deepseek-ai/deepseek-coder-7b-instruct-v1.5",
        #"mergekit-community/Qwen3-7B-Instruct",
        #"Ygz-08123/Qwen3-7B-Instruct-Q2_K-GGUF",
        #"Ygz-08123/Qwen3-7B-Instruct-Q4_K_M-GGUF",
        #"goodgooodboy/Qwen3-7B-Instruct-Q4_K_M-GGUF",
        #"HuggingFaceTB/SmolLM2-135M-Instruct",
        #"unsloth/SmolLM2-135M-Instruct",
        #"unsloth/SmolLM2-360M-Instruct",
        #"unsloth/SmolLM2-1.7B-Instruct",
        #"LiquidAI/LFM2.5-1.2B-Instruct",
        #"TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        #"OpenLLM-France/Luciole-1B-Instruct-1.1",
        #"tencent/Hunyuan-1.8B-Instruct",
        #"microsoft/Phi-4-mini-instruct",
        #"unsloth/Llama-3.2-3B-Instruct",
        #"TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",
        #"TheBlokeAI/Mixtral-tiny-GPTQ",
        #"mlx-community/SmolLM3-3B-4bit",
        #"unsloth/SmolLM2-1.7B-Instruct-bnb-4bit",
        #"nakue/SmolLM2-1.7B-W4A16-instruct",


    ]
    """
    ==========================================================================================
Model ID                            | Results              | Accuracy   | Total Time
------------------------------------------------------------------------------------------
Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF | ok ok ok ok ok       | 100.0%    | 9:51      
NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF | ok ok ok ok fail     |  80.0%    | 2:50      
NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF | ok ok ok ok ok       | 100.0%    | 5:02      
NikolayKozloff/gemma-3-12b-it-Q8_0-GGUF | ok ok ok ok ok       | 100.0%    | 5:57      
NikolayKozloff/gemma-3-12b-it-Q5_K_S-GGUF | ok ok ok ok ok       | 100.0%    | 5:44      
NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF | ok ok ok ok ok       | 100.0%    | 2:25      
NikolayKozloff/Mistral-Nemo-Instruct-2407-Q8_0-GGUF | fail fail fail fail fail |   0.0%    | 0:09      
Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF  | ok fail ok fail ok   |  60.0%    | 2:02      
Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF | ok ok ok ok ok       | 100.0%    | 1:31      
Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF   | ok ok ok ok ok       | 100.0%    | 1:04      
Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF | ok ok ok ok ok       | 100.0%    | 1:54      
unsloth/gemma-3-1b-it-unsloth-bnb-4bit | fail fail fail fail fail |   0.0%    | 0:07      
unsloth/gemma-3-1b-pt-unsloth-bnb-4bit | fail fail fail fail fail |   0.0%    | 0:01      
mlx-community/gemma-3-1b-it-4bit    | fail fail fail fail fail |   0.0%    | 0:00      
google/gemma-3n-E4B-it-litert-lm    | fail fail fail fail fail |   0.0%    | 0:00      
deepseek-ai/deepseek-coder-7b-instruct-v1.5 | fail fail fail fail fail |   0.0%    | 0:01      
lynnea1517/huihui-ai_gemma-3-27b-it-abliterated-Q8_0-GGUF | ok ok ok ok ok       | 100.0%    | 7:35      
paultimothymooney/gemma-3-27b-it-Q8_0-GGUF | ok ok ok ok ok       | 100.0%    | 8:19      
aminlouhichi/gemma-3-merged-GGUF-Q16 | ok ok ok ok ok       | 100.0%    | 2:19      
mergekit-community/Qwen3-7B-Instruct | fail fail fail fail fail |   0.0%    | 47:19     
Ygz-08123/Qwen3-7B-Instruct-Q2_K-GGUF | fail fail fail fail fail |   0.0%    | 10:44     
Ygz-08123/Qwen3-7B-Instruct-Q4_K_M-GGUF | fail fail fail fail fail |   0.0%    | 0:00      
goodgooodboy/Qwen3-7B-Instruct-Q4_K_M-GGUF | fail fail fail fail fail |   0.0%    | 0:00      
HuggingFaceTB/SmolLM2-135M-Instruct | fail fail fail fail fail |   0.0%    | 0:00      
unsloth/SmolLM2-135M-Instruct       | fail fail fail fail fail |   0.0%    | 0:00      
unsloth/SmolLM2-360M-Instruct       | fail fail fail fail fail |   0.0%    | 0:00      
unsloth/SmolLM2-1.7B-Instruct       | fail fail fail fail fail |   0.0%    | 0:00      
LiquidAI/LFM2.5-1.2B-Instruct       | fail fail fail fail fail |   0.0%    | 0:00      
TinyLlama/TinyLlama-1.1B-Chat-v1.0  | fail fail fail fail fail |   0.0%    | 0:00      
OpenLLM-France/Luciole-1B-Instruct-1.1 | fail fail fail fail fail |   0.0%    | 0:00      
tencent/Hunyuan-1.8B-Instruct       | fail fail fail fail fail |   0.0%    | 0:00      
microsoft/Phi-4-mini-instruct       | fail fail fail fail fail |   0.0%    | 0:00      
unsloth/Llama-3.2-3B-Instruct       | fail fail fail fail fail |   0.0%    | 0:00      
TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ | fail fail fail fail fail |   0.0%    | 0:00      
TheBlokeAI/Mixtral-tiny-GPTQ        | fail fail fail fail fail |   0.0%    | 0:00      
mlx-community/SmolLM3-3B-4bit       | fail fail fail fail fail |   0.0%    | 0:00      
unsloth/SmolLM2-1.7B-Instruct-bnb-4bit | fail fail fail fail fail |   0.0%    | 0:00      
nakue/SmolLM2-1.7B-W4A16-instruct   | fail fail fail fail fail |   0.0%    | 0:00      
==========================================================================================
    """

    for model_slice in [17,
        #10, 14,
        9999999]:
        print("=== CACHING MODELS ===")
        if True:
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
            try:
                for j in range(1 if i > 0 else 2):
                    start_time = time.time()
                    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"  [{start_timestamp}] Sending request {i + 1}/{len(questions)}...")
                    response = client.generate(model_id, q["question"], model_limit_seconds=request_timeout)
                    end_time = time.time()
                    duration = end_time - start_time
                    end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if i == 0 and j == 0:
                        continue
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