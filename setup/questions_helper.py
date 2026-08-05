import json


class QuestionsHelper:
    @staticmethod
    def get_questions1():
        return [
            {"question": "Calculate: 15 + 27. Answer with only the number.", "answer": "42"},
            {"question": "What is the capital city of Japan? Answer with only the city name.", "answer": "Tokyo"},
            {"question": "What is the next number in this sequence: 2, 4, 6, 8? Answer with only the number.",
             "answer": "10"},
            {
                "question": "Which of the following is programming language Mozilla, Terminator, Python, Outlook, Snake, Cloud? Answer with only one word.",
                "answer": "Python"},
            {"question": "Is the Earth flat or round? Answer with only one word: 'flat' or 'round'.", "answer": "round"}
        ]

    @staticmethod
    def get_questions2():
        return [
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

    import json

    @staticmethod
    def get_vacancy_json_questions():
        """Generates 50 vacancy extraction questions with increasing complexity."""
        questions = []
        companies = ["TechCorp", "DataSolutions", "AI Innovations", "CloudNine", "SoftWorks",
                     "DevHub", "CodeCraft", "ByteLogic", "NetSphere", "SysAdmin Pro"]
        countries = ["USA", "UK", "Germany", "Canada", "Australia",
                     "France", "Netherlands", "Poland", "Spain", "Italy"]
        cities = ["New York", "London", "Berlin", "Toronto", "Sydney",
                  "Paris", "Amsterdam", "Warsaw", "Madrid", "Rome"]
        titles = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Product Manager", "Frontend Developer",
                  "Backend Developer", "ML Engineer", "System Administrator", "QA Engineer", "Project Manager"]

        for i in range(50):
            complexity = i // 10  # 0 to 4

            if complexity == 0:
                keys = ["title", "company", "country", "city"]
            elif complexity == 1:
                keys = ["title", "company", "country", "city", "salary_min", "salary_max"]
            elif complexity == 2:
                keys = ["title", "company", "country", "city", "employment_type", "experience_min", "experience_max",
                        "remote"]
            elif complexity == 3:
                keys = ["title", "company", "country", "city", "salary_currency", "salary_period", "team_size",
                        "required_languages", "visa_sponsorship", "relocation"]
            else:
                keys = ["title", "company", "country", "city", "salary_min", "salary_max", "employment_type",
                        "experience_min", "experience_max", "remote", "visa_sponsorship", "required_languages"]

            # Generate vacancy text based on complexity
            text_parts = [f"We are hiring a {titles[i % 10]} at {companies[i % 10]}."]
            text_parts.append(f"The position is based in {cities[i % 10]}, {countries[i % 10]}.")

            if complexity >= 1:
                text_parts.append(f"The salary range is {50 + i}k to {80 + i}k per year.")
            if complexity >= 2:
                text_parts.append(f"This is a {['full-time', 'part-time', 'contract'][i % 3]} position.")
                text_parts.append(f"We require {1 + (i % 5)} to {3 + (i % 5)} years of experience.")
                text_parts.append(f"Remote work is {['allowed', 'not allowed', 'hybrid'][i % 3]}.")
            if complexity >= 3:
                text_parts.append(
                    f"Salary is paid in {['USD', 'EUR', 'GBP'][i % 3]} on a {['monthly', 'yearly'][i % 2]} basis.")
                text_parts.append(f"The team size is {10 + (i % 20)} people.")
                text_parts.append(f"Required languages: {['English', 'English, German', 'English, French'][i % 3]}.")
                text_parts.append(f"Visa sponsorship is {['available', 'not available'][i % 2]}.")
                text_parts.append(f"Relocation support is {['provided', 'not provided'][i % 2]}.")
            if complexity >= 4:
                text_parts.append(f"Minimum salary is {60 + i}000 and maximum is {90 + i}000.")
                text_parts.append(f"Experience required is between {2 + (i % 6)} and {8 + (i % 6)} years.")
                text_parts.append("We offer a dynamic work environment with cutting-edge technologies.")
                text_parts.append("Candidates must have strong problem-solving skills and a passion for innovation.")
                text_parts.append(
                    "The role involves collaborating with cross-functional teams to deliver high-quality software.")
                text_parts.append("We provide comprehensive health insurance and a flexible working schedule.")
                text_parts.append("Opportunities for professional growth and continuous learning are abundant.")
                text_parts.append("The ideal candidate will have a proven track record in similar roles.")
                text_parts.append("We value diversity and are an equal opportunity employer.")
                text_parts.append("Join us in shaping the future of technology and making a real impact.")

            vacancy_text = " ".join(text_parts)

            # Generate expected JSON
            expected = {}
            if "title" in keys: expected["title"] = titles[i % 10]
            if "company" in keys: expected["company"] = companies[i % 10]
            if "country" in keys: expected["country"] = countries[i % 10]
            if "city" in keys: expected["city"] = cities[i % 10]
            if "salary_min" in keys: expected["salary_min"] = f"{50 + i}k"
            if "salary_max" in keys: expected["salary_max"] = f"{80 + i}k"
            if "employment_type" in keys: expected["employment_type"] = ["full-time", "part-time", "contract"][i % 3]
            if "experience_min" in keys: expected["experience_min"] = str(1 + (i % 5))
            if "experience_max" in keys: expected["experience_max"] = str(3 + (i % 5))
            if "remote" in keys: expected["remote"] = ["allowed", "not allowed", "hybrid"][i % 3]
            if "salary_currency" in keys: expected["salary_currency"] = ["USD", "EUR", "GBP"][i % 3]
            if "salary_period" in keys: expected["salary_period"] = ["monthly", "yearly"][i % 2]
            if "team_size" in keys: expected["team_size"] = str(10 + (i % 20))
            if "required_languages" in keys: expected["required_languages"] = \
            ["English", "English, German", "English, French"][i % 3]
            if "visa_sponsorship" in keys: expected["visa_sponsorship"] = ["available", "not available"][i % 2]
            if "relocation" in keys: expected["relocation"] = ["provided", "not provided"][i % 2]

            keys_str = ", ".join([f'"{k}"' for k in keys])
            question_prompt = (
                f"====TEXT of VACANCY====\n{vacancy_text}\n====END TEXT====\n\n"
                f"Based on the vacancy text above, extract the following details and return ONLY a valid JSON object "
                f"with these exact keys: {keys_str}. Do not add any markdown formatting, extra text, or explanations. "
                f"EXACT EXPECTED JSON: {json.dumps(expected)}"
            )

            questions.append({
                "question": question_prompt,
                "expected_json": expected,
                "summary": f"Extract {', '.join(keys)} from vacancy {i + 1}."
            })

        return questions