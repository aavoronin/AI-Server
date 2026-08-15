import time
import json
from datetime import datetime
from typing import Any
from pathlib import Path

from ai_clients.TextToTextClient import TextToTextClient
from setup.running_model_utils import (
    format_time, parse_json_safely, compare_values, print_json_failures
)


def shorten_vacancy_text(v_name: str, v_text: str) -> str:
    vacancy_slice = [
        ("LinkedIn_Vacancy", "About the job", "Unlock hiring insights", 8),
        ("Hirify_Vacancy", "Job description", "", 3),
    ]

    for prefix, start_marker, end_marker, num_first_rows in vacancy_slice:
        if v_name.startswith(prefix):
            start_idx = 0
            if start_marker:
                idx = v_text.find(start_marker)
                if idx != -1:
                    start_idx = idx

            end_idx = len(v_text)
            if end_marker:
                idx = v_text.rfind(end_marker)
                if idx != -1:
                    end_idx = idx + len(end_marker)

            sliced_text = v_text[start_idx:end_idx].strip()

            if num_first_rows > 0:
                original_lines = v_text.splitlines()
                first_rows = "\n".join(original_lines[:num_first_rows])
                return (first_rows + "\n" + sliced_text).strip()

            return sliced_text

    return v_text


def get_prompt_and_model(version) -> tuple[list[str], list[str], str]:
    test_models = [
        "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF|GPU|32768",
        "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
        # "NikolayKozloff/gemma-3-12b-it-Q5_K_S-GGUF|GPU|32768",
        # "NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF|GPU|32768",
        # "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|16384",
        # "Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF|GPU|16384",
        # "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|GPU|16384",
        # "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|GPU|16384",
        # "Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF|GPU|16384",
        # "Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF|GPU|16384",
        # "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
    ]

    '''
        "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF",
        "lynnea1517/huihui-ai_gemma-3-27b-it-abliterated-Q8_0-GGUF",
        "paultimothymooney/gemma-3-27b-it-Q8_0-GGUF",
        "aminlouhichi/gemma-3-merged-GGUF-Q16",
        "Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",
        #"NikolayKozloff/gemma-3-12b-it-Q5_K_S-GGUF",
        "NikolayKozloff/gemma-3-12b-it-Q8_0-GGUF",
    '''

    if version == 1:
        prompt_files = [
            "PROMPT.txt"
        ]
        test_models = [
            "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF|GPU|32768",
            "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
        ]
        vacancies_folder = r"C:\Py\AI-Server\test_cases\test_vacancies\01"

    elif version == 2:
        prompt_files = [
            "PROMPT_01.txt",
            "PROMPT_02.txt",
            "PROMPT_03.txt",
            "PROMPT_04.txt",
            "PROMPT_05.txt",
            "PROMPT_06.txt",
            "PROMPT_07.txt"
        ]
        test_models = [
            "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q4_K_M|GPU|32768",
            "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|32768",
        ]
        vacancies_folder = r"C:\Py\AI-Server\test_cases\test_vacancies\01"
    elif version == 3:
        prompt_files = [
            "PROMPT_SIMPLE.txt"
        ]
        test_models = [
            "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF|GPU|32768",
            "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
            "rktmeister/Meta-Llama-3.1-8B-Instruct-Q5_K_M-GGUF|GPU|32768",
            "matrixportalx/Llama-3.3-8B-Instruct-128K-Q5_K_M-GGUF|GPU|32768",
            #"Medvedko/Huihui-Qwen3-8B-abliterated-v2-Q5_K_M-GGUF|GPU|32768",
            # "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|CPU|32768",

            #"Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q4_K_M",
            #"Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q5_K_M",
            #"Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q8_0",
            #"NikolayKozloff/Llama-3.3-8B-Instruct-Q8_0-GGUF|GPU|32768",
            #"matrixportalx/Llama-3.3-8B-Instruct-Q4_K_M-GGUF|GPU|32768",
            #"majentik/gemma-4-26B-A4B-it-RotorQuant-GGUF-Q4_K_M|CPU|32768",
            "NikolayKozloff/Qwen3-8B-Q8_0-GGUF|GPU|32768",
            #"DarkKitsune/qwen3.5-9b-qworus-Q5-imat-GGUF|GPU|32768",

            #"aminlouhichi/gemma-3-merged-GGUF-Q16|GPU|32768",
            # "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF|CPU|32768",
            # "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
            # "majentik/Nemotron-3-Nano-4B-RotorQuant-GGUF-Q4_K_M|GPU|32768",
            # "majentik/Nemotron-3-Nano-4B-RotorQuant-GGUF-Q4_K_M|CPU|32768",
            # "unsloth/Llama-3.2-3B-Instruct|GPU|32768",
            # "rktmeister/Meta-Llama-3.1-8B-Instruct-Q5_K_M-GGUF|CPU|32768",
            # "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|CPU|32768",
            # "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|CPU|32768",

            #"Ma7ee7/Qwen3.8_4B_Distilled_GGUF|GPU|32768|Q4_K_M",
            #"Ma7ee7/Qwen3.8_4B_Distilled_GGUF|GPU|32768|Q5_K_M",
            #"Ma7ee7/Qwen3.8_4B_Distilled_GGUF|GPU|32768|Q8_0",

            #"Disya/Huihui-Qwen3-4B-Thinking-2507-abliterated-Q8_0-GGUF",

            #"FORNAX20/gemma-4-26B-A4B-it-uncensored-Q5_K_M-GGUF|CPU|32768"
            #"Darkknight535/gemma-4-31B-it-abliterated-Q5_K_M-GGUF|CPU|32768"

            # "unsloth/Llama-3.2-3B-Instruct|CPU|32768",
            # "aminlouhichi/gemma-3-merged-GGUF-Q16|GPU|32768",
            # "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
            #"soob3123/GrayLine-Gemma3-12B-Q4_K_M-GGUF|GPU|32768",
            #"NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF|CPU|32768",
            #"Medvedko/gemma-3-12b-it-heretic-v2-Q4_K_M-GGUF|GPU|32768",
            #"nocturne23/gemma-3-12b-it-Q4_K_M-GGUF|GPU|32768",
            #"majentik/gemma-4-12B-it-TurboQuant-GGUF-Q4_K_M|GPU|32768",
            #"majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|32768",
            #"majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|GPU|32768",
            #"majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|GPU|32768",
            # "soob3123/GrayLine-Gemma3-12B-Q4_K_M-GGUF|GPU|32768",
            # "Medvedko/gemma-3-12b-it-heretic-v2-Q4_K_M-GGUF|GPU|32768",
            # "nocturne23/gemma-3-12b-it-Q4_K_M-GGUF|GPU|32768",
            # "NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF|GPU|24576",
            # "NikolayKozloff/gemma-3-12b-it-Q6_K-GGUF|CPU|24576",
            # "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q5_K_M|GPU|24576",
            # "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|GPU|24576",
            # "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q4_K_M|GPU|24576",
            # "majentik/gemma-4-12B-it-TurboQuant-GGUF-Q4_K_M|GPU|24576",
        ]
        vacancies_folder = r"C:\Py\AI-Server\test_cases\test_vacancies\02"
    elif version == 4:
        prompt_files = [
            "PROMPT_SIMPLE.txt"
        ]
        test_models = [
            "NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF|GPU|32768",
            "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
            "rktmeister/Meta-Llama-3.1-8B-Instruct-Q5_K_M-GGUF|GPU|32768",
            "matrixportalx/Llama-3.3-8B-Instruct-128K-Q5_K_M-GGUF|GPU|32768",
            "Medvedko/Huihui-Qwen3-8B-abliterated-v2-Q5_K_M-GGUF|GPU|32768",

            "Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q4_K_M",
            "Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q5_K_M",
            "Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q8_0",
            # "NikolayKozloff/Llama-3.3-8B-Instruct-Q8_0-GGUF|GPU|32768",
            "matrixportalx/Llama-3.3-8B-Instruct-Q4_K_M-GGUF|GPU|32768",
            "NikolayKozloff/Qwen3-8B-Q8_0-GGUF|GPU|32768",

            "neopolita/Qwen3.6-11B-A3B-Niwaki-4bit-GGUF|GPU|32768|Q4_K_M",
            "neopolita/Qwen3.6-11B-A3B-Niwaki-4bit-GGUF|GPU|32768|UD-Q3K",

            "neopolita/Qwen3.6-11B-A3B-Niwaki-4bit-GGUF|GPU|32768|Q4_K_M",
            "neopolita/Qwen3.6-11B-A3B-Niwaki-4bit-GGUF|GPU|32768|UD-Q3K",

            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q6_K",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q8_0",

            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ3_M",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ3_S",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ4_NL",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ4_XS",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q2_K",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q3_K_L",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q3_K_M",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q3_K_S",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q4_0",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q4_K_M",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q4_K_S",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q5_0",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q5_K_M",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q5_K_S",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q6_K",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q8_0",

            "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|CPU|32768",
            "majentik/gemma-4-26B-A4B-it-RotorQuant-GGUF-Q5_K_M|CPU|32768",
            "majentik/gemma-4-26B-A4B-it-RotorQuant-GGUF-Q8_0|CPU|32768",

            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|CPU|32768|Q6_K",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|CPU|32768|Q8_0",

        ]
        vacancies_folder = r"C:\Py\AI-Server\test_cases\test_vacancies\03"
    else:
        prompt_files = []
        test_models = []
        vacancies_folder = r"C:\Py\AI-Server\test_cases\test_vacancies\01"
    return prompt_files, test_models, vacancies_folder


def warmup_model(client, model_id, timeout):
    """1) Cache/warm-up model by sending a simple request."""
    start_time = time.time()
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{start_timestamp} Starting ping -- {model_id}")
    client.generate(model_id, "2+2", model_limit_seconds=timeout)
    duration = time.time() - start_time
    end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{end_timestamp} Ping time: {duration:.2f}s -- {model_id}")


def make_vacancy_request(client, model_id, full_prompt, timeout, start_time):
    """2) Make a single generation request to the model."""
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{start_timestamp} Starting generate -- {model_id}")
    response = client.generate(model_id, full_prompt, model_limit_seconds=timeout)
    duration = time.time() - start_time
    generated_text = response.get("generated_text", "")
    if not isinstance(generated_text, str):
        generated_text = str(generated_text)
    end_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return generated_text, duration, end_timestamp


def parse_and_merge_json(generated_text, combined_parsed_dict):
    """3) Parse JSON response and merge into combined dict."""
    parsed_dict = parse_json_safely(generated_text)
    if parsed_dict is not None:
        for key, value in parsed_dict.items():
            if key not in combined_parsed_dict:
                combined_parsed_dict[key] = value
    return parsed_dict


def calculate_vacancy_score(expected_json, combined_parsed_dict):
    """4) Calculate score for a vacancy by comparing expected vs actual."""
    keys_in_expected = len(expected_json)
    correct_keys = 0.0
    if keys_in_expected > 0:
        for key, expected_value in expected_json.items():
            actual_value = combined_parsed_dict.get(key)
            score = compare_values(actual_value, expected_value)
            correct_keys += score
    score = correct_keys / keys_in_expected if keys_in_expected > 0 else 0.0
    return score, keys_in_expected, correct_keys


def update_model_summary(model_id, total_keys, total_correct_keys, total_time,
                         vacancy_scores, model_summaries):
    """5) Update and print model summary."""
    avg_score = (total_correct_keys / total_keys) if total_keys > 0 else 0.0
    time_str = format_time(total_time)

    print(f"\n--- Summary for {model_id} ---")
    for vs in vacancy_scores:
        print(f"  {vs['vacancy']:<40} | Score: {vs['score']:.2f} | Time: {vs['time']:.2f}s")
    print(f"  {'AVERAGE':<40} | Score: {avg_score:.2%} | Total Time: {time_str}")

def run_models_on_vacancies(version):
    """Benchmark models on real vacancy text files against ground truth JSONs."""
    VACANCY_TIMEOUT = 60 * 20
    VACANCY_TIMEOUT_0 = 3600

    prompt_files, test_models, vacancies_dir = get_prompt_and_model(version)
    vacancies_path = Path(vacancies_dir)

    client = TextToTextClient()

    # Find all vacancy txt files and their corresponding result jsons
    vacancies = []
    for txt_file in sorted(vacancies_path.glob("*.txt")):
        result_json_file = txt_file.with_name(txt_file.stem + "_result.json")
        if result_json_file.exists():
            vacancies.append((txt_file, result_json_file))

    if not vacancies:
        print(f"No matching vacancy/result pairs found in {vacancies_dir}")
        return

    print("=== RUNNING VACANCIES BENCHMARK ===")
    print(f"Total Models: {len(test_models)}")
    print(f"Total Vacancies: {len(vacancies)}")

    model_summaries = []

    for model_id in test_models:
        print(f"\n{'=' * 80}")
        print(f"Testing Model: {model_id}")
        print(f"{'=' * 80}")

        total_keys = 0
        total_correct_keys = 0.0
        total_time = 0.0
        vacancy_scores = []

        for i, (txt_file, result_json_file) in enumerate(vacancies):
            vacancy_name = txt_file.stem
            vacancy_text = txt_file.read_text(encoding='utf-8')
            vacancy_text = shorten_vacancy_text(vacancy_name, vacancy_text)

            try:
                with open(result_json_file, 'r', encoding='utf-8') as f:
                    expected_json = json.load(f)
            except json.JSONDecodeError:
                print(f"[{vacancy_name}] ERROR: Invalid JSON in {result_json_file.name}. Scoring as 0.00")
                expected_json = {}
            except Exception as e:
                print(f"[{vacancy_name}] ERROR: Failed to read {result_json_file.name}: {e}. Scoring as 0.00")
                expected_json = {}

            combined_parsed_dict = {}
            total_vacancy_time = 0.0

            for p_file in prompt_files:
                prompt_path = vacancies_path.parent / p_file
                if not prompt_path.exists():
                    continue
                prompt_text = prompt_path.read_text(encoding='utf-8')
                full_prompt = prompt_text + "\n" + vacancy_text

                print(
                    f"  [{p_file}] Vacancy Length: {len(vacancy_text)} chars | "
                    f"Total Prompt Length: {len(full_prompt)} chars")

                if i == 0:
                    warmup_model(client, model_id, VACANCY_TIMEOUT_0)

                start_time = time.time()
                try:
                    generated_text, duration, end_timestamp = make_vacancy_request(
                        client, model_id, full_prompt, VACANCY_TIMEOUT, start_time)
                    total_vacancy_time += duration

                    parsed_dict = parse_and_merge_json(generated_text, combined_parsed_dict)

                    valid_json = 'Yes' if parsed_dict is not None else 'No'
                    print(
                        f"{end_timestamp}  [{p_file}] Time: {duration:.2f}s | Valid JSON: {valid_json}")

                except Exception as e:
                    duration = time.time() - start_time
                    total_vacancy_time += duration
                    print(f"  [{p_file}] ERROR: {str(e)} | Time: {duration:.2f}s")

            # Evaluate combined result
            score, keys_in_expected, correct_keys = calculate_vacancy_score(
                expected_json, combined_parsed_dict)

            total_keys += keys_in_expected
            total_correct_keys += correct_keys
            total_time += total_vacancy_time

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
        update_model_summary(model_id, total_keys, total_correct_keys,
                             total_time, vacancy_scores, model_summaries)

    print_vacancies_model_summary(model_summaries)


def print_vacancies_model_summary(model_summaries: list[Any]):
    # Final Overall Summary
    print("\n" + "=" * 90)
    print(f"{'Model ID':<50} | {'Avg Score':<12} | {'Total Time':<10}")
    print("-" * 90)
    for ms in model_summaries:
        print(f"{ms['model_id']:<50} | {ms['avg_score']:>6.2%}    | {ms['time_str']:<10}")
    print("=" * 90)