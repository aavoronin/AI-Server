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
        {
            "question": "What is the name of the variable in this code: 'for i in range(10):\n    print(i)'? Answer with only the variable name.",
            "answer": "i"
        },
        {
            "question": "What is the table name without schema mentioned in this Query: 'SELECT A, B, C FROM dbo.employees'? Answer with only the table name.",
            "answer": "employees"
        },
        {
            "question": "What is the schema name for the table mentioned in this Query: 'SELECT A, B, C FROM hr.employees'? Answer with only the schema name.",
            "answer": "hr"
        },
        {
            "question": "How many loops are in this code: 'while True:\n    for i in range(10):\n        for j in range(i): \n            print(i, j)'? Answer with only the number.",
            "answer": "3"
        },
        {
            "question": "Is the Earth flat or round? Answer with only one word: 'flat' or 'round'.",
            "answer": "round"
        },
        {
            "question": "What is the length of the list in this code: 'my_list = [1, 2, 3, 4, 5]'? Answer with only the number.",
            "answer": "5"
        },
        {
            "question": "What is the key associated with the value 'apple' in this dictionary: \"{'fruit': 'apple', 'color': 'red'}\"? Answer with only the key name.",
            "answer": "fruit"
        },
        {
            "question": "How many columns are being selected in this query: 'SELECT id, name, age, email FROM users'? Answer with only the number.",
            "answer": "4"
        },
        {
            "question": "What is the name of the function defined in this code: 'def calculate_sum(a, b): return a + b'? Answer with only the function name.",
            "answer": "calculate_sum"
        },
        {
            "question": "What is the column name used in the WHERE clause of this query: 'SELECT * FROM orders WHERE status = \"shipped\"'? Answer with only the column name.",
            "answer": "status"
        },
        {
            "question": "What is the boolean value of the expression '5 > 10' in Python? Answer with only 'True' or 'False'.",
            "answer": "False"
        },
        {
            "question": "What is the key for the age value in this JSON: '{\"name\": \"John\", \"age\": 30}'? Answer with only the key name.",
            "answer": "age"
        },
        {
            "question": "What is the result of '10 % 3' in Python? Answer with only the number.",
            "answer": "1"
        },
        {
            "question": "What aggregate function is used in this query: 'SELECT COUNT(*) FROM employees'? Answer with only the function name.",
            "answer": "COUNT"
        },
        {
            "question": "What is the index of the first element in a Python list? Answer with only the number.",
            "answer": "0"
        },
        {
            "question": "What is the attribute used to specify the link destination in this code: '<a href=\"https://example.com\">Link</a>'? Answer with only the attribute name.",
            "answer": "href"
        },
        {
            "question": "What is the output of `len('hello')` in Python? Answer with only the number.",
            "answer": "5"
        },
        {
            "question": "What SQL keyword is used to filter records? Answer with only the keyword.",
            "answer": "WHERE"
        },
        {
            "question": "What is the value of `x` after this code: 'x = 10; x += 5'? Answer with only the number.",
            "answer": "15"
        },
        {
            "question": "What HTML tag is used to create a paragraph? Answer with only the tag name without brackets.",
            "answer": "p"
        },
        {
            "question": "What is the result of `2 ** 3` in Python? Answer with only the number.",
            "answer": "8"
        },
        {
            "question": "What SQL clause is used to sort the result-set? Answer with only the clause name.",
            "answer": "ORDER BY"
        },
        {
            "question": "What is the value associated with the key 'city' in this JSON: '{\"city\": \"Paris\", \"country\": \"France\"}'? Answer with only the value.",
            "answer": "Paris"
        },
        {
            "question": "What method is used to add an element to the end of a list in Python? Answer with only the method name.",
            "answer": "append"
        },
        {
            "question": "What is the result of `17 // 5` in Python? Answer with only the number.",
            "answer": "3"
        },
        {
            "question": "What SQL command is used to remove a table entirely? Answer with only the command.",
            "answer": "DROP"
        },
        {
            "question": "What is the data type of `[1, 2, 3]` in Python? Answer with only the type name.",
            "answer": "list"
        },
        {
            "question": "What attribute is used to specify an image source in HTML? Answer with only the attribute name.",
            "answer": "src"
        },
        {
            "question": "What is the result of `bool(0)` in Python? Answer with only 'True' or 'False'.",
            "answer": "False"
        },
        {
            "question": "What keyword is used to define a function in Python? Answer with only the keyword.",
            "answer": "def"
        }
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
        "Bhuvneesh/gemma-4-E4B-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-4-E4B-it-Q5_K_M-GGUF",
        "Bhuvneesh/gemma-3-4b-it-Q8_0-GGUF",
        "Bhuvneesh/gemma-3-12b-it-Q5_K_M-GGUF",  # Note: 12B Q5 is ~10-11GB, fits tightly in 12GB VRAM
        #"unsloth/gemma-4-12b-it-GGUF",
        "unsloth/gemma-3-1b-it-unsloth-bnb-4bit",
        "unsloth/gemma-3-1b-pt-unsloth-bnb-4bit",
        "mlx-community/gemma-3-1b-it-4bit",
        "google/gemma-3n-E4B-it-litert-lm",

        #"deepseek-ai/deepseek-coder-1.3b-instruct",
        #"Qwen/Qwen2-1.5B-Instruct",
        #"Qwen/Qwen2.5-1.5B-Instruct",
        #"Qwen/Qwen2.5-3B-Instruct",
        #"Qwen/Qwen2.5-7B-Instruct",

        #"Qwen/Qwen2.5-Coder-3B-Instruct",
        "deepseek-ai/deepseek-coder-7b-instruct-v1.5",

        "Bhuvneesh/gemma-3-27b-it-Q5_K_M-GGUF",

        "mergekit-community/Qwen3-7B-Instruct",
        "Ygz-08123/Qwen3-7B-Instruct-Q2_K-GGUF",
        "Ygz-08123/Qwen3-7B-Instruct-Q4_K_M-GGUF",
        "goodgooodboy/Qwen3-7B-Instruct-Q4_K_M-GGUF",
        #"lm-kit/qwen-3-14b-instruct-gguf",

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

        # ✅ Recommended Quantized Formats (GGUF / GPTQ / BNB-4bit) of the above models
        "TheBloke/TinyLlama-1.1B-Chat-v0.3-GPTQ",
        "TheBlokeAI/Mixtral-tiny-GPTQ",
        "mlx-community/SmolLM3-3B-4bit",
        "unsloth/SmolLM2-1.7B-Instruct-bnb-4bit",
        "nakue/SmolLM2-1.7B-W4A16-instruct",
    ]

    for model_slice in [10, 9999999]:
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
    # Make list of models distinct
    test_models = list(dict.fromkeys(test_models))

    results = []
    total_start_time = time.time()

    # Save tuples of (question, model, answer, time_taken)
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
            # Mark as failed for all questions and continue to next model
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
        i: int | Literal[0],
        k: int,
        model_id: str,
        model_results: dict[str, str | list[Any] | float],
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

            # Save tuple for the new table
            answers_list.append((q["question"], model_id, generated_text.strip(), duration))
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
        answers_list.append((q["question"], model_id, "-", duration))

        if i == 0 and "500" in error_msg:
            print(f"  Q: {q['question'][:70]}... -> fail (500 Error on 1st question, aborting model)")
            model_results["scores"].append("fail")
            model_results["times"].append(duration)
            model_results["total_time"] += duration
            # Mark remaining questions as fail with 0 time
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
    """
    Proposes a prompt template tailored to the specific model family to enforce
    exact, concise answers without additional text, reasoning, or explanations.
    """
    model_id_lower = model_id.lower()
    question = q["question"]

    if "gemma" in model_id_lower:
        # Gemma models respond exceptionally well to the /no_think suffix
        prompt_template = "{question} /no_think"
    elif "qwen" in model_id_lower:
        # Qwen models tend to repeat the prompt and explain. Need strong negative constraints.
        prompt_template = "{question}\n\nOutput ONLY the exact answer requested. Do not repeat the question, do not add punctuation, and do not provide any explanations."
    elif "deepseek" in model_id_lower:
        # DeepSeek Coder tends to output "Answer: " or repeat the prompt.
        prompt_template = "{question}\n\nRespond with EXACTLY the requested value and nothing else. Do not output 'Answer:', do not repeat the question, and do not explain."
    elif any(x in model_id_lower for x in
             ["smollm", "tinyllama", "luciole", "hunyuan", "phi", "llama", "mixtral", "olmo", "lfm"]):
        # General small instruct models respond better to positive constraints.
        prompt_template = "{question}\n\nRespond with EXACTLY the requested value (e.g., a single word or number) and absolutely nothing else."
    else:
        # Fallback for unspecified models: strong, clear, positive constraint.
        prompt_template = "{question}\n\nOutput ONLY the exact answer requested, with no additional text, explanations, or punctuation."

    return prompt_template.format(question=question)


def print_answers(answers_list: list[Any]):
    # Print the new table format before the final result
    print("\n" + "=" * 110)
    print("ANSWERS BY QUESTION")
    print("=" * 110)

    # Group by question
    answers_by_question = defaultdict(list)
    for q_text, model_id, answer, time_taken in answers_list:
        answers_by_question[q_text].append((model_id, answer, time_taken))

    for q_text, model_answers in answers_by_question.items():
        print(f"\n{q_text}")
        for model_id, answer, time_taken in model_answers:
            clean_answer = "".join(c for c in answer[:800] if c.isprintable())
            print(f"  {model_id} ({time_taken:.2f}s): {clean_answer[:200]}")
    print("\n" + "=" * 110)