import time
import json
from datetime import datetime
from typing import Any
from pathlib import Path

from ai_clients.TextToTextClient import TextToTextClient
from setup.running_model_utils import (
    format_time, format_value, parse_json_safely, compare_values, print_json_failures
)

# Scoring matrix for version >= 4
# Rows = expected level, Columns = generated level
PROFICIENCY_SCORE_MATRIX = {
    "expert":       {"expert": 6, "required": 3, "nice-to_have": 1},
    "required":     {"expert": 3, "required": 4, "nice-to_have": 1},
    "nice-to_have": {"expert": 1, "required": 1, "nice-to_have": 2},
}

# Keys that use proficiency matrix scoring
PROFICIENCY_LEVEL_KEYS = {"expert", "required", "nice-to_have"}

# Max points per expected level
PROFICIENCY_MAX_POINTS = {
    "expert": 6,
    "required": 4,
    "nice-to_have": 2,
}


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
            "NikolayKozloff/Qwen3-8B-Q8_0-GGUF|GPU|32768",
        ]
        vacancies_folder = r"C:\Py\AI-Server\test_cases\test_vacancies\02"
    elif version == 4:
        prompt_files = [
            "PROMPT_SIMPLE3.txt"
        ]
        test_models = [
            #"NikolayKozloff/gemma-3-1b-it-Q8_0-GGUF|GPU|32768",
            "NikolayKozloff/gemma-3-4b-it-Q8_0-GGUF|GPU|32768",
            "rktmeister/Meta-Llama-3.1-8B-Instruct-Q5_K_M-GGUF|GPU|32768",
            "matrixportalx/Llama-3.3-8B-Instruct-128K-Q5_K_M-GGUF|GPU|32768",
            "majentik/gemma-4-12B-it-RotorQuant-GGUF-Q5_K_M|CPU|32768",

            #"NikolayKozloff/Llama-3.3-8B-Instruct-Q8_0-GGUF|GPU|32768",
            #"Medvedko/Huihui-Qwen3-8B-abliterated-v2-Q5_K_M-GGUF|GPU|32768",

            "majentik/gemma-4-26B-A4B-it-RotorQuant-GGUF-Q5_K_M|CPU|32768",
            #"majentik/gemma-4-26B-A4B-it-RotorQuant-GGUF-Q8_0|CPU|32768",

            "majentik/gemma-4-12B-RotorQuant-GGUF-Q8_0|CPU|32768",

            #"Jackxuanxuan/Gemma-4-31B-JANG-Q8_4M-CRACK-GGUF|CPU|32768",
            "KikoCis/gemma-4-31b-it-Q3_K_M-GGUF|CPU|32768",

            #"Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q4_K_M",
            "Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q5_K_M",
            #"Ma7ee7/Qwen3.8_1.2B_LFM_Distillation_GGUF|GPU|32768|Q8_0",
            #"matrixportalx/Llama-3.3-8B-Instruct-Q4_K_M-GGUF|GPU|32768",
            #"NikolayKozloff/Qwen3-8B-Q8_0-GGUF|GPU|32768",

            "neopolita/Qwen3.6-11B-A3B-Niwaki-4bit-GGUF|GPU|32768|Q4_K_M",
            #"neopolita/Qwen3.6-11B-A3B-Niwaki-4bit-GGUF|GPU|32768|UD-Q3K",

            "mradermacher/Llama-3.3-8B-Instruct-128K-Jbliterated-i1-GGUF|GPU|32768|Q6_K",
            "mradermacher/Llama-3.3-8B-Instruct-128K-Jbliterated-i1-GGUF|GPU|32768|Q5_K_M",
            "mradermacher/Llama-3.3-8B-Instruct-128K-Jbliterated-i1-GGUF|GPU|32768|Q4_K_M",

            #"KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q6_K",
            #"KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q8_0",
            #"KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q5_K_M",
            #"KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ3_M",
            #"KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ3_S",
            #"KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ4_NL",
            #KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|IQ4_XS",
            #"KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q3_K_M",
            "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|GPU|32768|Q4_K_M",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|CPU|32768|Q6_K",
            # "KevinJK51/Qwen3.6-12B-IQ-Ultra-Heretic-Uncensored-Thinking-V2-Hightop-GGUF|CPU|32768|Q8_0",

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


def calculate_vacancy_score(expected_json, combined_parsed_dict, version=1):
    """4) Calculate score for a vacancy by comparing expected vs actual."""
    if version <= 3:
        keys_in_expected = len(expected_json)
        correct_keys = 0.0
        if keys_in_expected > 0:
            for key, expected_value in expected_json.items():
                actual_value = combined_parsed_dict.get(key)
                score = compare_values(actual_value, expected_value)
                correct_keys += score
        score = correct_keys / keys_in_expected if keys_in_expected > 0 else 0.0
        return score, keys_in_expected, correct_keys
    else:
        # version >= 4: use proficiency matrix scoring for level keys,
        # compare_values for other keys
        return calculate_vacancy_score_matrix(expected_json, combined_parsed_dict)


def calculate_vacancy_score_matrix(expected_json, combined_parsed_dict):
    """Calculate score using proficiency matrix for version >= 4."""
    levels = ["expert", "required", "nice-to_have"]

    # Build expected skill->level mapping (normalized to lowercase)
    expected_skills = {}
    for level in levels:
        if level in expected_json and isinstance(expected_json[level], list):
            for skill in expected_json[level]:
                skill_norm = skill.strip().lower()
                expected_skills[skill_norm] = level

    # Build generated skill->level mapping (normalized to lowercase)
    generated_skills = {}
    for level in levels:
        if level in combined_parsed_dict and isinstance(combined_parsed_dict[level], list):
            for skill in combined_parsed_dict[level]:
                skill_norm = skill.strip().lower()
                generated_skills[skill_norm] = level

    # Calculate score for proficiency matrix keys
    total_points = 0.0
    actual_points = 0.0

    for skill_norm, expected_level in expected_skills.items():
        max_points = PROFICIENCY_MAX_POINTS[expected_level]
        total_points += max_points

        generated_level = generated_skills.get(skill_norm)
        if generated_level is not None and generated_level in PROFICIENCY_SCORE_MATRIX.get(expected_level, {}):
            actual_points += PROFICIENCY_SCORE_MATRIX[expected_level][generated_level]
        # If skill is not found in generated, it gets 0 points

    # Calculate score for other keys (not proficiency level keys) using compare_values
    for key, expected_value in expected_json.items():
        if key in PROFICIENCY_LEVEL_KEYS:
            continue
        total_points += 1.0
        actual_value = combined_parsed_dict.get(key)
        score = compare_values(actual_value, expected_value)
        actual_points += score

    score = actual_points / total_points if total_points > 0 else 0.0
    return score, total_points, actual_points


def print_json_failures_v4(expected_json, combined_parsed_dict):
    """Print failures for version >= 4, showing per-skill breakdown for proficiency keys."""
    levels = ["expert", "required", "nice-to_have"]

    # Build expected skill->level mapping
    expected_skills = {}
    for level in levels:
        if level in expected_json and isinstance(expected_json[level], list):
            for skill in expected_json[level]:
                skill_norm = skill.strip().lower()
                expected_skills[skill_norm] = level

    # Build generated skill->level mapping
    generated_skills = {}
    for level in levels:
        if level in combined_parsed_dict and isinstance(combined_parsed_dict[level], list):
            for skill in combined_parsed_dict[level]:
                skill_norm = skill.strip().lower()
                generated_skills[skill_norm] = level

    # Print per-skill breakdown for proficiency keys
    for skill_norm, expected_level in expected_skills.items():
        max_points = PROFICIENCY_MAX_POINTS[expected_level]
        generated_level = generated_skills.get(skill_norm)

        if generated_level is not None and generated_level in PROFICIENCY_SCORE_MATRIX.get(expected_level, {}):
            points = PROFICIENCY_SCORE_MATRIX[expected_level][generated_level]
        else:
            points = 0

        if points < max_points:
            gen_display = generated_level if generated_level else "missing"
            print(f"    {skill_norm}: {points} of {max_points} ({expected_level}|{gen_display})")

    # Print other keys as before
    for key, expected_value in expected_json.items():
        if key in PROFICIENCY_LEVEL_KEYS:
            continue
        expected_disp = format_value(expected_value)
        if combined_parsed_dict is not None and key in combined_parsed_dict:
            actual_value = combined_parsed_dict[key]
            actual_disp = format_value(actual_value)
            score = compare_values(actual_value, expected_value)
            if score < 1.0:
                if score == 0.5:
                    print(f'    "{key}": partial ("{actual_disp}"|"{expected_disp}")')
                else:
                    print(f'    "{key}": fail ("{actual_disp}"|"{expected_disp}")')
        else:
            score = compare_values(None, expected_value)
            if score < 1.0:
                print(f'    "{key}": fail (|"{expected_disp}")')


def update_model_summary(model_id, total_keys, total_correct_keys, total_time,
                         vacancy_scores, model_summaries):
    """5) Update and print model summary."""
    avg_score = (total_correct_keys / total_keys) if total_keys > 0 else 0.0
    time_str = format_time(total_time)

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


def run_models_on_vacancies(version):
    """Benchmark models on real vacancy text files against ground truth JSONs."""
    VACANCY_TIMEOUT = 60 * 20
    VACANCY_TIMEOUT_0 = 3600 * 6
    verbose = True
    vacancies_limit = 1

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
            if i >= vacancies_limit:
                continue
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
                    if verbose:
                        print(20 * '=' + ' START PROMPT ' + 20 * '=')
                        print(full_prompt)
                        print(20 * '=' + ' END PROMPT ' + 20 * '=')

                start_time = time.time()
                try:
                    generated_text, duration, end_timestamp = make_vacancy_request(
                        client, model_id, full_prompt, VACANCY_TIMEOUT, start_time)
                    total_vacancy_time += duration

                    parsed_dict = parse_and_merge_json(generated_text, combined_parsed_dict)
                    if i == 0:
                        print(20 * '=' + ' START RESPONSE ' + 20 * '=')
                        if parsed_dict is not None:
                            pretty_json_string = json.dumps(parsed_dict, indent=4)
                            print(pretty_json_string)
                        else:
                            print(generated_text)
                        print(20 * '=' + ' END RESPONSE ' + 20 * '=')

                    valid_json = 'Yes' if parsed_dict is not None else 'No'
                    print(
                        f"{end_timestamp}  [{p_file}] Time: {duration:.2f}s | Valid JSON: {valid_json}")

                except Exception as e:
                    duration = time.time() - start_time
                    total_vacancy_time += duration
                    print(f"  [{p_file}] ERROR: {str(e)} | Time: {duration:.2f}s")

            # Evaluate combined result
            score, keys_in_expected, correct_keys = calculate_vacancy_score(
                expected_json, combined_parsed_dict, version)

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
                if version >= 4:
                    print_json_failures_v4(expected_json, combined_parsed_dict)
                else:
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