import json
from typing import Any

NULL_EQUIVALENTS = {"null", "", "no", "none", "-"}

PROFICIENCY_PARTIAL_MATCHES = {
    frozenset({"nice-to-have", "required"}),
    frozenset({"required", "expert"})
}

COUNTRY_SYNONYMS = {
    "us": "usa", "united states": "usa", "united states of america": "usa", "america": "usa", "usa": "usa",
    "can": "canada", "ca": "canada", "canada": "canada",
    "uk": "uk", "united kingdom": "uk", "great britain": "uk", "britain": "uk", "gb": "uk", "england": "uk",
    "de": "germany", "deutschland": "germany", "germany": "germany",
    "fr": "france", "france": "france",
    "in": "india", "bharat": "india", "india": "india",
    "au": "australia", "aussie": "australia", "australia": "australia",
    "jp": "japan", "japan": "japan",
    "cn": "china", "prc": "china", "china": "china",
    "ru": "russia", "russian federation": "russia", "russia": "russia",
    "ir": "iran", "iran": "iran",
    "worldwide": "global", "world": "global", "anywhere": "global", "remote": "global", "global": "global",
}


def format_time(total_elapsed):
    total_elapsed = int(total_elapsed)
    h, rem = divmod(total_elapsed, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def format_value(val):
    return str(val).replace('\n', ' ').replace('"', "'") if val is not None else ""


def compare_values(actual_value, expected_value):
    if isinstance(expected_value, list):
        if not isinstance(actual_value, list):
            actual_value = [actual_value] if actual_value is not None else []

        act_list = [str(v).strip().lower() for v in actual_value]
        exp_list = [str(v).strip().lower() for v in expected_value]

        act_syn = sorted([COUNTRY_SYNONYMS.get(v, v) for v in act_list])
        exp_syn = sorted([COUNTRY_SYNONYMS.get(v, v) for v in exp_list])

        if act_syn == exp_syn:
            return 1.0

        act_nulls = all(v in NULL_EQUIVALENTS for v in act_list) if act_list else True
        exp_nulls = all(v in NULL_EQUIVALENTS for v in exp_list) if exp_list else True
        if act_nulls and exp_nulls:
            return 1.0

        return 0.0
    else:
        actual_str = str(actual_value).strip().lower() if actual_value is not None else ""
        expected_str = str(expected_value).strip().lower()

        if actual_str == expected_str:
            return 1.0

        if actual_str in NULL_EQUIVALENTS and expected_str in NULL_EQUIVALENTS:
            return 1.0

        actual_syn = COUNTRY_SYNONYMS.get(actual_str, actual_str)
        expected_syn = COUNTRY_SYNONYMS.get(expected_str, expected_str)
        if actual_syn == expected_syn:
            return 1.0

        if frozenset({actual_str, expected_str}) in PROFICIENCY_PARTIAL_MATCHES:
            return 0.5

        return 0.0


def compare_json_with_expected(expected_json, parsed_dict):
    for key, expected_value in expected_json.items():
        expected_disp = format_value(expected_value)
        if parsed_dict is not None and key in parsed_dict:
            actual_value = parsed_dict[key]
            actual_disp = format_value(actual_value)
            score = compare_values(actual_value, expected_value)
            if score == 1.0:
                print(f'    "{key}": ok ("{actual_disp}")')
            elif score == 0.5:
                print(f'    "{key}": partial ("{actual_disp}"|"{expected_disp}")')
            else:
                print(f'    "{key}": fail ("{actual_disp}"|"{expected_disp}")')
        else:
            score = compare_values(None, expected_value)
            if score == 1.0:
                print(f'    "{key}": ok (|"{expected_disp}")')
            elif score == 0.5:
                print(f'    "{key}": partial (|"{expected_disp}")')
            else:
                print(f'    "{key}": fail (|"{expected_disp}")')


def print_json_failures(expected_json, parsed_dict):
    for key, expected_value in expected_json.items():
        expected_disp = format_value(expected_value)
        if parsed_dict is not None and key in parsed_dict:
            actual_value = parsed_dict[key]
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
                if score == 0.5:
                    print(f'    "{key}": partial (|"{expected_disp}")')
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
        if not isinstance(json_output, str):
            return None

        start_idx = json_output.find('{')
        end_idx = json_output.rfind('}')

        if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
            return None

        parsed_output = json_output[start_idx:end_idx + 1]
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

    correct_keys = 0.0
    total_keys = len(expected_json)
    for key, expected_value in expected_json.items():
        actual_value = parsed.get(key)
        score = compare_values(actual_value, expected_value)
        correct_keys += score

    return correct_keys / total_keys if total_keys > 0 else 0.0