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

    @staticmethod
    def get_vacancy_json_questions():
        """Generates 50 hardcoded vacancy extraction questions with increasing complexity."""

        # Format: (vacancy_text, keys_to_extract, example_format_dict)
        raw_data = [
            # 1-10: Short (3-5 lines), simple subjects
            ("We are looking for a Junior Python Developer to join our team. The role is fully remote. You must be located in the USA or Canada. We do not sponsor visas.",
             ["Title", "CandidateCountry", "VisaSponsorship"],
             {"Title": "Example Role", "CandidateCountry": ["USA"], "VisaSponsorship": "no"}),

            ("Senior Data Engineer needed. You will work with Python, SQL, and Apache Airflow. Experience with dbt is a nice-to-have. No prior experience with AWS is required.",
             ["Title", "Python", "SQL", "Apache_Airflow", "dbt", "AWS"],
             {"Title": "Example Role", "Python": "required", "SQL": "required", "Apache_Airflow": "required",
              "dbt": "nice-to-have", "AWS": "no"}),

            ("Join us as a Frontend Developer. We offer 25 days of paid time off, health insurance, and a 5000 learning budget.",
             ["Title", "PaidTimeOffDays", "HealthInsurance", "LearningBudget"],
             {"Title": "Example Role", "PaidTimeOffDays": 20, "HealthInsurance": "yes", "LearningBudget": "1000"}),

            ("Senior DevOps Engineer role. Minimum 5 years of experience required. Master's degree preferred.",
             ["Title", "MinYearsExperience", "EducationLevel"],
             {"Title": "Example Role", "MinYearsExperience": 3, "EducationLevel": "bachelor"}),

            ("We are seeking a Machine Learning Engineer based in London, UK. The timezone is GMT. Salary ranges from 70,000 to 90,000 GBP annually. Relocation is offered with a 5000 budget.",
             ["Title", "EmployerCity", "EmployerCountry", "EmployerTimezone", "SalaryMin", "SalaryMax",
              "SalaryCurrency", "SalaryPeriod", "RelocationOffered", "RelocationBudget"],
             {"Title": "Example Role", "EmployerCity": "City", "EmployerCountry": ["USA"], "EmployerTimezone": "EST",
              "SalaryMin": "50000", "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "RelocationOffered": "yes", "RelocationBudget": "1000"}),

            ("Product Manager opening. The hiring process includes 3 interview rounds and a technical assessment. No coding challenge is required. We need to fill this role immediately.",
             ["Title", "InterviewRounds", "TechnicalAssessment", "CodingChallenge", "Urgency"],
             {"Title": "Example Role", "InterviewRounds": 2, "TechnicalAssessment": "yes", "CodingChallenge": "yes",
              "Urgency": "flexible"}),

            ("Contract Software Engineer needed for a 12-month project. Probation period is 1 month. Notice period is 2 weeks. Working hours are 40 per week.",
             ["Title", "ContractType", "ContractDurationMonths", "ProbationPeriodMonths", "NoticePeriodWeeks",
              "WorkingHoursPerWeek"],
             {"Title": "Example Role", "ContractType": "permanent", "ContractDurationMonths": 6,
              "ProbationPeriodMonths": 3, "NoticePeriodWeeks": 4, "WorkingHoursPerWeek": 37.5}),

            ("Join our startup as a Data Scientist. We are a team of 15 people reporting to the VP of Data. We are hiring 2 people for this role.",
             ["Title", "CompanyStage", "TeamSize", "ReportingTo", "NumberOfOpenPositions"],
             {"Title": "Example Role", "CompanyStage": "enterprise", "TeamSize": 50, "ReportingTo": "Manager",
              "NumberOfOpenPositions": 1}),

            ("We are looking for a Senior QA Engineer. Required languages: English, German. A background check is required, but no drug screening. An NDA is required, but no non-compete.",
             ["Title", "RequiredLanguages", "BackgroundCheck", "DrugScreening", "NDARequired", "NonCompeteRequired"],
             {"Title": "Example Role", "RequiredLanguages": ["English"], "BackgroundCheck": "no",
              "DrugScreening": "yes", "NDARequired": "no", "NonCompeteRequired": "yes"}),

            ("Data Engineer role posted on LinkedIn. Job ID is 123456789. Apply at https://careers.co/apply. Posted 4 days ago, over 100 applicants.",
             ["Title", "JobId", "VacancySite", "ApplyURL", "PublicationDate", "ApplicantsCount"],
             {"Title": "Example Role", "JobId": "000", "VacancySite": "Indeed", "ApplyURL": "url",
              "PublicationDate": "1 day ago", "ApplicantsCount": "50"}),

            # 11-20: Medium (6-10 lines), varied subjects
            ("DWH Developer needed. You will work with Star Schema, Snowflake Schema, and Data Vault. Experience with dbt and Apache Airflow is required. Knowledge of Kimball Methodology is a nice-to-have.",
             ["Title", "Star_Schema", "Snowflake_Schema", "Data_Vault", "dbt", "Apache_Airflow", "Kimball_Methodology"],
             {"Title": "Example Role", "Star_Schema": "required", "Snowflake_Schema": "no", "Data_Vault": "no",
              "dbt": "no", "Apache_Airflow": "no", "Kimball_Methodology": "no"}),

            ("Machine Learning Engineer. You will work with NLP, Computer Vision, and LLMs. Experience with PyTorch and TensorFlow is required. Familiarity with RAG and Prompt Engineering is a nice-to-have.",
             ["Title", "NLP", "Computer_Vision", "LLMs", "PyTorch", "TensorFlow", "RAG", "Prompt_Engineering"],
             {"Title": "Example Role", "NLP": "no", "Computer_Vision": "no", "LLMs": "no", "PyTorch": "no",
              "TensorFlow": "no", "RAG": "no", "Prompt_Engineering": "no"}),

            ("DevOps Engineer. Required: Docker, Kubernetes, Terraform, Ansible. Nice-to-have: Jenkins, GitHub Actions. No experience with ArgoCD needed.",
             ["Title", "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "GitHub_Actions", "ArgoCD"],
             {"Title": "Example Role", "Docker": "no", "Kubernetes": "no", "Terraform": "no", "Ansible": "no",
              "Jenkins": "no", "GitHub_Actions": "no", "ArgoCD": "no"}),

            ("We are hiring a Senior Software Engineer. The role is fully remote, based in the USA. Salary is 120k-150k USD per year. We offer health insurance, 401k, and 20 days PTO. You need 5+ years of experience and a Bachelor's degree. The tech stack includes Python, SQL, and AWS.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "HealthInsurance", "RetirementPlan", "PaidTimeOffDays", "MinYearsExperience", "EducationLevel", "Python",
              "SQL", "AWS"],
             {"Title": "Example Role", "EmploymentType": "office", "CandidateCountry": ["UK"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "EUR", "SalaryPeriod": "year", "HealthInsurance": "no",
              "RetirementPlan": "no", "PaidTimeOffDays": 10, "MinYearsExperience": 2, "EducationLevel": "high-school",
              "Python": "no", "SQL": "no", "AWS": "no"}),

            ("Contract Data Analyst needed for a 6-month project. Probation is 1 month, notice period is 2 weeks. Working 40 hours/week. The company is a scale-up in the Financial Services industry. Team size is 10, reporting to the Head of Data. We are hiring 1 person. Minimum 3 years experience, Bachelor's degree required. Tech: SQL, Python, Tableau.",
             ["Title", "ContractType", "ContractDurationMonths", "ProbationPeriodMonths", "NoticePeriodWeeks",
              "WorkingHoursPerWeek", "CompanyStage", "CompanyIndustry", "TeamSize", "ReportingTo",
              "NumberOfOpenPositions", "MinYearsExperience", "EducationLevel", "SQL", "Python", "Tableau"],
             {"Title": "Example Role", "ContractType": "permanent", "ContractDurationMonths": 12,
              "ProbationPeriodMonths": 3, "NoticePeriodWeeks": 4, "WorkingHoursPerWeek": 37.5,
              "CompanyStage": "startup", "CompanyIndustry": "Tech", "TeamSize": 5, "ReportingTo": "Manager",
              "NumberOfOpenPositions": 2, "MinYearsExperience": 1, "EducationLevel": "master", "SQL": "no",
              "Python": "no", "Tableau": "no"}),

            ("Backend Developer role. Required languages: English. Background check required, no drug screening, NDA required, no non-compete. Job ID: 987654. Posted on Indeed. Apply at https://apply.co. Posted 2 days ago, 50 applicants. Tech: Java, Spring Boot, PostgreSQL.",
             ["Title", "RequiredLanguages", "BackgroundCheck", "DrugScreening", "NDARequired", "NonCompeteRequired",
              "JobId", "VacancySite", "ApplyURL", "PublicationDate", "ApplicantsCount", "Java", "Spring_Boot",
              "PostgreSQL"],
             {"Title": "Example Role", "RequiredLanguages": ["German"], "BackgroundCheck": "no", "DrugScreening": "yes",
              "NDARequired": "no", "NonCompeteRequired": "yes", "JobId": "000", "VacancySite": "LinkedIn",
              "ApplyURL": "url", "PublicationDate": "1 day ago", "ApplicantsCount": "10", "Java": "no",
              "Spring_Boot": "no", "PostgreSQL": "no"}),

            ("AI Research Scientist. You will work with Deep Learning, Neural Networks, NLP, and LLMs. Experience with PyTorch, TensorFlow, and RAG is required. Nice-to-have: Prompt Engineering, Fine-Tuning. Soft skills: Communication, Teamwork, Problem Solving, Critical Thinking.",
             ["Title", "Deep_Learning", "Neural_Networks", "NLP", "LLMs", "PyTorch", "TensorFlow", "RAG",
              "Prompt_Engineering", "Fine_Tuning", "Communication", "Teamwork", "Problem_Solving", "Critical_Thinking"],
             {"Title": "Example Role", "Deep_Learning": "no", "Neural_Networks": "no", "NLP": "no", "LLMs": "no",
              "PyTorch": "no", "TensorFlow": "no", "RAG": "no", "Prompt_Engineering": "no", "Fine_Tuning": "no",
              "Communication": "no", "Teamwork": "no", "Problem_Solving": "no", "Critical_Thinking": "no"}),

            ("Full Stack Data Warehouse Developer. Remote, USA. Salary 100k-130k USD/year. Health insurance, 401k, 25 days PTO, 5000 learning budget. 5+ years experience, Bachelor's degree. Tech: Python, SQL, dbt, Apache Airflow, Star Schema, Snowflake Schema. 3 interview rounds, technical assessment, no coding challenge. Urgency: within-1-month.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "HealthInsurance", "RetirementPlan", "PaidTimeOffDays", "LearningBudget", "MinYearsExperience",
              "EducationLevel", "Python", "SQL", "dbt", "Apache_Airflow", "Star_Schema", "Snowflake_Schema",
              "InterviewRounds", "TechnicalAssessment", "CodingChallenge", "Urgency"],
             {"Title": "Example Role", "EmploymentType": "office", "CandidateCountry": ["UK"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "EUR", "SalaryPeriod": "year", "HealthInsurance": "no",
              "RetirementPlan": "no", "PaidTimeOffDays": 10, "LearningBudget": "1000", "MinYearsExperience": 2,
              "EducationLevel": "master", "Python": "no", "SQL": "no", "dbt": "no", "Apache_Airflow": "no",
              "Star_Schema": "no", "Snowflake_Schema": "no", "InterviewRounds": 2, "TechnicalAssessment": "no",
              "CodingChallenge": "yes", "Urgency": "immediate"}),

            ("We are hiring a Frontend Developer. Location: remote, USA. Salary: 80000-110000 USD per year. Benefits include: Health insurance, 20 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 3 years. Tech stack: React, TypeScript, CSS, HTML, Webpack, Vite. Soft skills: Communication, Teamwork, Adaptability.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "React", "TypeScript", "CSS", "HTML", "Webpack", "Vite", "Communication", "Teamwork", "Adaptability"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "React": "required",
              "TypeScript": "required", "CSS": "required", "HTML": "required", "Webpack": "required",
              "Vite": "required", "Communication": "required", "Teamwork": "required", "Adaptability": "required"}),

            ("We are hiring a Data Engineer. Location: hybrid, UK. Salary: 90000-120000 GBP per year. Benefits include: 401k, learning budget 2000. Hiring process: 4 rounds, no coding challenge. Requirements: Master's, 5 years. Tech stack: Python, SQL, Spark, Kafka, AWS, dbt. Soft skills: Problem Solving, Critical Thinking.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Python", "SQL", "Spark", "Kafka", "AWS", "dbt", "Problem_Solving", "Critical_Thinking"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Python": "required",
              "SQL": "required", "Spark": "required", "Kafka": "required", "AWS": "required", "dbt": "required",
              "Problem_Solving": "required", "Critical_Thinking": "required"}),

            # 21-30: Medium-Long (10-15 lines), complex subjects
            ("We are hiring a DevOps Engineer. Location: remote, Canada. Salary: 100000-140000 CAD per year. Benefits include: Stock options, unlimited PTO. Hiring process: 2 rounds, system design. Requirements: Bachelor's, 4 years. Tech stack: Docker, Kubernetes, Terraform, Ansible, Jenkins. Soft skills: Leadership, Time Management.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "Leadership", "Time_Management"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Docker": "required",
              "Kubernetes": "required", "Terraform": "required", "Ansible": "required", "Jenkins": "required",
              "Leadership": "required", "Time_Management": "required"}),

            ("We are hiring a Product Manager. Location: office, Germany. Salary: 70000-95000 EUR per year. Benefits include: Health, dental, 15 days PTO. Hiring process: 3 rounds, case study. Requirements: Bachelor's, 6 years. Tech stack: Jira, Confluence, Figma, SQL. Soft skills: Negotiation, Empathy, Decision Making.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Jira", "Confluence", "Figma", "SQL", "Negotiation", "Empathy", "Decision_Making"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Jira": "required",
              "Confluence": "required", "Figma": "required", "SQL": "required", "Negotiation": "required",
              "Empathy": "required", "Decision_Making": "required"}),

            ("We are hiring a QA Automation Engineer. Location: remote, Australia. Salary: 85000-105000 AUD per year. Benefits include: Gym membership, 22 days PTO. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: Python, Selenium, PyTest, Jenkins, Docker. Soft skills: Attention to Detail, Patience.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Python", "Selenium", "PyTest", "Jenkins", "Docker", "Attention_to_Detail", "Patience"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Python": "required",
              "Selenium": "required", "PyTest": "required", "Jenkins": "required", "Docker": "required",
              "Attention_to_Detail": "required", "Patience": "required"}),

            ("We are hiring a Machine Learning Engineer. Location: hybrid, France. Salary: 60000-85000 EUR per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 4 rounds, technical assessment. Requirements: PhD, 2 years. Tech stack: Python, PyTorch, TensorFlow, NLP, LLMs. Soft skills: Creativity, Analytical Thinking.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Python", "PyTorch", "TensorFlow", "NLP", "LLMs", "Creativity", "Analytical_Thinking"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Python": "required",
              "PyTorch": "required", "TensorFlow": "required", "NLP": "required", "LLMs": "required",
              "Creativity": "required", "Analytical_Thinking": "required"}),

            ("We are hiring a Backend Developer. Location: remote, Netherlands. Salary: 75000-95000 EUR per year. Benefits include: Meal allowance, 20 days PTO. Hiring process: 3 rounds, take-home assignment. Requirements: Bachelor's, 4 years. Tech stack: Java, Spring Boot, PostgreSQL, Redis, Kafka. Soft skills: Collaboration, Work Ethic.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Java", "Spring_Boot", "PostgreSQL", "Redis", "Kafka", "Collaboration", "Work_Ethic"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Java": "required",
              "Spring_Boot": "required", "PostgreSQL": "required", "Redis": "required", "Kafka": "required",
              "Collaboration": "required", "Work_Ethic": "required"}),

            ("We are hiring a UI/UX Designer. Location: hybrid, Spain. Salary: 50000-70000 EUR per year. Benefits include: Health, 18 days PTO, learning budget. Hiring process: 3 rounds, portfolio review. Requirements: Bachelor's, 3 years. Tech stack: Figma, Sketch, Adobe XD, User Research. Soft skills: Empathy, Communication, Creativity.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Figma", "Sketch", "Adobe_XD", "User_Research", "Empathy", "Communication", "Creativity"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Figma": "required",
              "Sketch": "required", "Adobe_XD": "required", "User_Research": "required", "Empathy": "required",
              "Communication": "required", "Creativity": "required"}),

            ("We are hiring a Cloud Architect. Location: remote, USA. Salary: 150000-200000 USD per year. Benefits include: Stock options, 30 days PTO. Hiring process: 4 rounds, architecture review. Requirements: Master's, 8 years. Tech stack: AWS, Azure, GCP, Terraform, Kubernetes. Soft skills: Strategic Thinking, Leadership.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "AWS", "Azure", "GCP", "Terraform", "Kubernetes", "Strategic_Thinking", "Leadership"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "AWS": "required",
              "Azure": "required", "GCP": "required", "Terraform": "required", "Kubernetes": "required",
              "Strategic_Thinking": "required", "Leadership": "required"}),

            ("We are hiring a Security Engineer. Location: office, UK. Salary: 90000-120000 GBP per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 5 years. Tech stack: Python, Bash, Linux, Wireshark, Splunk. Soft skills: Critical Thinking, Attention to Detail.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Python", "Bash", "Linux", "Wireshark", "Splunk", "Critical_Thinking", "Attention_to_Detail"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Python": "required",
              "Bash": "required", "Linux": "required", "Wireshark": "required", "Splunk": "required",
              "Critical_Thinking": "required", "Attention_to_Detail": "required"}),

            ("We are hiring a Mobile Developer. Location: remote, Canada. Salary: 80000-110000 CAD per year. Benefits include: Health, 20 days PTO, gym. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: Swift, Kotlin, React Native, Firebase. Soft skills: Adaptability, Problem Solving.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Swift", "Kotlin", "React_Native", "Firebase", "Adaptability", "Problem_Solving"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Swift": "required",
              "Kotlin": "required", "React_Native": "required", "Firebase": "required", "Adaptability": "required",
              "Problem_Solving": "required"}),

            ("We are hiring a Site Reliability Engineer. Location: hybrid, Germany. Salary: 85000-115000 EUR per year. Benefits include: Unlimited PTO, stock options. Hiring process: 3 rounds, system design. Requirements: Bachelor's, 4 years. Tech stack: Go, Python, Kubernetes, Prometheus, Grafana. Soft skills: Stress Management, Teamwork.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Go", "Python", "Kubernetes", "Prometheus", "Grafana", "Stress_Management", "Teamwork"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Go": "required",
              "Python": "required", "Kubernetes": "required", "Prometheus": "required", "Grafana": "required",
              "Stress_Management": "required", "Teamwork": "required"}),

            # 31-40: Long (15-20 lines), highly detailed subjects
            ("We are hiring a Business Analyst. Location: office, Australia. Salary: 70000-90000 AUD per year. Benefits include: Health, 22 days PTO. Hiring process: 2 rounds, case study. Requirements: Bachelor's, 2 years. Tech stack: SQL, Excel, Tableau, Power BI. Soft skills: Communication, Analytical Thinking.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "SQL", "Excel", "Tableau", "Power_BI", "Communication", "Analytical_Thinking"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "SQL": "required",
              "Excel": "required", "Tableau": "required", "Power_BI": "required", "Communication": "required",
              "Analytical_Thinking": "required"}),

            ("We are hiring a Network Engineer. Location: remote, France. Salary: 65000-85000 EUR per year. Benefits include: Health, 20 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 5 years. Tech stack: Cisco, Juniper, Python, BGP, OSPF. Soft skills: Problem Solving, Attention to Detail.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Cisco", "Juniper", "Python", "BGP", "OSPF", "Problem_Solving", "Attention_to_Detail"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Cisco": "required",
              "Juniper": "required", "Python": "required", "BGP": "required", "OSPF": "required",
              "Problem_Solving": "required", "Attention_to_Detail": "required"}),

            ("We are hiring a Scrum Master. Location: hybrid, Netherlands. Salary: 70000-90000 EUR per year. Benefits include: Health, 25 days PTO, learning budget. Hiring process: 2 rounds, behavioral. Requirements: Bachelor's, 4 years. Tech stack: Jira, Confluence, Agile, Scrum. Soft skills: Leadership, Empathy, Communication.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Jira", "Confluence", "Agile", "Scrum", "Leadership", "Empathy", "Communication"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Jira": "required",
              "Confluence": "required", "Agile": "required", "Scrum": "required", "Leadership": "required",
              "Empathy": "required", "Communication": "required"}),

            ("We are hiring a Database Administrator. Location: office, Spain. Salary: 60000-80000 EUR per year. Benefits include: Health, 401k, 20 days PTO. Hiring process: 3 rounds, technical assessment. Requirements: Bachelor's, 5 years. Tech stack: PostgreSQL, MySQL, Oracle, SQL Server. Soft skills: Attention to Detail, Problem Solving.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "PostgreSQL", "MySQL", "Oracle", "SQL_Server", "Attention_to_Detail", "Problem_Solving"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "PostgreSQL": "required",
              "MySQL": "required", "Oracle": "required", "SQL_Server": "required", "Attention_to_Detail": "required",
              "Problem_Solving": "required"}),

            ("We are hiring a Technical Writer. Location: remote, USA. Salary: 70000-90000 USD per year. Benefits include: Health, 20 days PTO, remote work. Hiring process: 2 rounds, writing test. Requirements: Bachelor's, 2 years. Tech stack: Markdown, Git, Confluence, Jira. Soft skills: Written Communication, Attention to Detail.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Markdown", "Git", "Confluence", "Jira", "Written_Communication", "Attention_to_Detail"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Markdown": "required",
              "Git": "required", "Confluence": "required", "Jira": "required", "Written_Communication": "required",
              "Attention_to_Detail": "required"}),

            ("We are hiring a Game Developer. Location: office, UK. Salary: 60000-85000 GBP per year. Benefits include: Health, 20 days PTO, game allowance. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: C++, Unreal Engine, Unity, C#. Soft skills: Creativity, Teamwork, Problem Solving.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "C_Plus_Plus", "Unreal_Engine", "Unity", "C_Sharp", "Creativity", "Teamwork", "Problem_Solving"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "C_Plus_Plus": "required",
              "Unreal_Engine": "required", "Unity": "required", "C_Sharp": "required", "Creativity": "required",
              "Teamwork": "required", "Problem_Solving": "required"}),

            ("We are hiring a Systems Administrator. Location: hybrid, Canada. Salary: 75000-95000 CAD per year. Benefits include: Health, 22 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 4 years. Tech stack: Linux, Windows, Bash, PowerShell, Ansible. Soft skills: Problem Solving, Time Management.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Linux", "Windows", "Bash", "PowerShell", "Ansible", "Problem_Solving", "Time_Management"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Linux": "required",
              "Windows": "required", "Bash": "required", "PowerShell": "required", "Ansible": "required",
              "Problem_Solving": "required", "Time_Management": "required"}),

            ("We are hiring a Data Scientist. Location: remote, Germany. Salary: 80000-110000 EUR per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 4 rounds, technical assessment. Requirements: Master's, 3 years. Tech stack: Python, R, SQL, Machine Learning, Pandas. Soft skills: Analytical Thinking, Communication.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Python", "R", "SQL", "Machine_Learning", "Pandas", "Analytical_Thinking", "Communication"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Python": "required",
              "R": "required", "SQL": "required", "Machine_Learning": "required", "Pandas": "required",
              "Analytical_Thinking": "required", "Communication": "required"}),

            ("We are hiring a Frontend Architect. Location: remote, USA. Salary: 160000-210000 USD per year. Benefits include: Stock options, 30 days PTO. Hiring process: 4 rounds, architecture review. Requirements: Master's, 8 years. Tech stack: React, TypeScript, Node.js, GraphQL, AWS. Soft skills: Leadership, Strategic Thinking.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "React", "TypeScript", "Node_js", "GraphQL", "AWS", "Leadership", "Strategic_Thinking"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "React": "required",
              "TypeScript": "required", "Node_js": "required", "GraphQL": "required", "AWS": "required",
              "Leadership": "required", "Strategic_Thinking": "required"}),

            ("We are hiring an Embedded Systems Engineer. Location: office, UK. Salary: 70000-95000 GBP per year. Benefits include: Health, 20 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 5 years. Tech stack: C, C++, RTOS, ARM, Linux. Soft skills: Attention to Detail, Problem Solving.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "C", "C_Plus_Plus", "RTOS", "ARM", "Linux", "Attention_to_Detail", "Problem_Solving"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "C": "required",
              "C_Plus_Plus": "required", "RTOS": "required", "ARM": "required", "Linux": "required",
              "Attention_to_Detail": "required", "Problem_Solving": "required"}),

            # 41-50: Very Long (20+ lines), comprehensive subjects
            ("We are hiring an IT Support Specialist. Location: office, Australia. Salary: 50000-65000 AUD per year. Benefits include: Health, 15 days PTO. Hiring process: 2 rounds, practical test. Requirements: High-school, 1 year. Tech stack: Windows, macOS, Active Directory, Office 365. Soft skills: Customer Service, Patience.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Windows", "macOS", "Active_Directory", "Office_365", "Customer_Service", "Patience"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Windows": "required",
              "macOS": "required", "Active_Directory": "required", "Office_365": "required",
              "Customer_Service": "required", "Patience": "required"}),

            ("We are hiring a Blockchain Developer. Location: remote, Switzerland. Salary: 100000-150000 CHF per year. Benefits include: Crypto bonuses, 25 days PTO. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: Solidity, Rust, Ethereum, Web3, Smart Contracts. Soft skills: Analytical Thinking, Problem Solving.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Solidity", "Rust", "Ethereum", "Web3", "Smart_Contracts", "Analytical_Thinking", "Problem_Solving"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Solidity": "required",
              "Rust": "required", "Ethereum": "required", "Web3": "required", "Smart_Contracts": "required",
              "Analytical_Thinking": "required", "Problem_Solving": "required"}),

            ("We are hiring a Growth Hacker. Location: hybrid, Netherlands. Salary: 65000-85000 EUR per year. Benefits include: Health, 20 days PTO, performance bonus. Hiring process: 3 rounds, case study. Requirements: Bachelor's, 3 years. Tech stack: SQL, Python, Google Analytics, A/B Testing. Soft skills: Creativity, Analytical Thinking.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "SQL", "Python", "Google_Analytics", "A_B_Testing", "Creativity", "Analytical_Thinking"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "SQL": "required",
              "Python": "required", "Google_Analytics": "required", "A_B_Testing": "required", "Creativity": "required",
              "Analytical_Thinking": "required"}),

            ("We are hiring a Solutions Architect. Location: remote, USA. Salary: 140000-190000 USD per year. Benefits include: Stock options, 30 days PTO. Hiring process: 4 rounds, architecture review. Requirements: Master's, 7 years. Tech stack: AWS, Azure, GCP, Terraform, Microservices. Soft skills: Strategic Thinking, Communication.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "AWS", "Azure", "GCP", "Terraform", "Microservices", "Strategic_Thinking", "Communication"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "AWS": "required",
              "Azure": "required", "GCP": "required", "Terraform": "required", "Microservices": "required",
              "Strategic_Thinking": "required", "Communication": "required"}),

            ("We are hiring a Quality Assurance Lead. Location: hybrid, UK. Salary: 80000-110000 GBP per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 3 rounds, technical assessment. Requirements: Bachelor's, 6 years. Tech stack: Python, Selenium, Cypress, Jenkins, Jira. Soft skills: Leadership, Attention to Detail.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Python", "Selenium", "Cypress", "Jenkins", "Jira", "Leadership", "Attention_to_Detail"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Python": "required",
              "Selenium": "required", "Cypress": "required", "Jenkins": "required", "Jira": "required",
              "Leadership": "required", "Attention_to_Detail": "required"}),

            ("We are hiring a Full Stack Engineer. Location: remote, Canada. Salary: 90000-120000 CAD per year. Benefits include: Health, 20 days PTO, learning budget. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 4 years. Tech stack: JavaScript, TypeScript, React, Node.js, PostgreSQL. Soft skills: Teamwork, Problem Solving.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "JavaScript", "TypeScript", "React", "Node_js", "PostgreSQL", "Teamwork", "Problem_Solving"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "JavaScript": "required",
              "TypeScript": "required", "React": "required", "Node_js": "required", "PostgreSQL": "required",
              "Teamwork": "required", "Problem_Solving": "required"}),

            ("We are hiring a Machine Learning Ops Engineer. Location: remote, Germany. Salary: 85000-115000 EUR per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 4 years. Tech stack: Python, Docker, Kubernetes, MLflow, AWS. Soft skills: Problem Solving, Automation.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Python", "Docker", "Kubernetes", "MLflow", "AWS", "Problem_Solving", "Automation"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Python": "required",
              "Docker": "required", "Kubernetes": "required", "MLflow": "required", "AWS": "required",
              "Problem_Solving": "required", "Automation": "required"}),

            ("We are hiring a Chief Technology Officer. Location: hybrid, USA. Salary: 200000-300000 USD per year. Benefits include: Equity, 40 days PTO, executive benefits. Hiring process: 3 rounds, executive interview. Requirements: Master's, 15 years. Tech stack: Strategic Planning, Team Leadership, Architecture. Soft skills: Leadership, Strategic Thinking, Vision.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "Strategic_Planning", "Team_Leadership", "Architecture", "Leadership", "Strategic_Thinking", "Vision"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "Strategic_Planning": "required",
              "Team_Leadership": "required", "Architecture": "required", "Leadership": "required",
              "Strategic_Thinking": "required", "Vision": "required"}),

            ("We are hiring a Cybersecurity Analyst. Location: office, Canada. Salary: 75000-95000 CAD per year. Benefits include: Health, 20 days PTO, certification budget. Hiring process: 3 rounds, technical assessment. Requirements: Bachelor's, 3 years. Tech stack: SIEM, Wireshark, Python, Linux, Firewall Management. Soft skills: Analytical Thinking, Attention to Detail.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "SIEM", "Wireshark", "Python", "Linux", "Firewall_Management", "Analytical_Thinking",
              "Attention_to_Detail"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "SIEM": "required",
              "Wireshark": "required", "Python": "required", "Linux": "required", "Firewall_Management": "required",
              "Analytical_Thinking": "required", "Attention_to_Detail": "required"}),

            ("We are hiring a Robotics Engineer. Location: hybrid, Germany. Salary: 80000-110000 EUR per year. Benefits include: Health, 25 days PTO, relocation support. Hiring process: 4 rounds, practical test. Requirements: Master's, 5 years. Tech stack: C++, ROS, Python, MATLAB, Computer Vision. Soft skills: Problem Solving, Innovation, Teamwork.",
             ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency", "SalaryPeriod",
              "C_Plus_Plus", "ROS", "Python", "MATLAB", "Computer_Vision", "Problem_Solving", "Innovation", "Teamwork"],
             {"Title": "Example Role", "EmploymentType": "remote", "CandidateCountry": ["USA"], "SalaryMin": "50000",
              "SalaryMax": "75000", "SalaryCurrency": "USD", "SalaryPeriod": "year", "C_Plus_Plus": "required",
              "ROS": "required", "Python": "required", "MATLAB": "required", "Computer_Vision": "required",
              "Problem_Solving": "required", "Innovation": "required", "Teamwork": "required"})
        ]

        questions = []
        for idx, (vacancy_text, keys, example_format) in enumerate(raw_data):
            keys_str = ", ".join([f'"{k}"' for k in keys])

            prompt = (
                f"====TEXT of VACANCY====\n{vacancy_text}\n====END TEXT====\n\n"
                f"ROLE & TASK: You are an expert technical recruiter and data extraction AI. Analyze the job description and extract specific details.\n"
                f"Extract the following details and return ONLY a valid JSON object with these exact keys: {keys_str}. "
                f"Do not add any markdown formatting, extra text, or explanations. Do not wrap the JSON in markdown code blocks (no ```json). "
                f"Example JSON format (values are examples, extract the ACTUAL values from the text): {json.dumps(example_format)}"
            )

            questions.append({
                "question": prompt,
                "expected_json": example_format,
                # Note: The evaluation will check if the model extracted the REAL values from the text, not the example values. Wait, the example format has example values. The evaluation function needs to know the REAL expected values.
                # Let's fix this: The example format should have placeholder values, but `expected_json` must have the REAL values for scoring.
                "summary": f"Extract details from vacancy {idx + 1}."
            })

        # To properly score, we need to separate the example format from the expected real values.
        # Let's redefine the raw_data to include real_expected_values.

        real_data = [
            # 1-10
            ("We are looking for a Junior Python Developer to join our team. The role is fully remote. You must be located in the USA or Canada. We do not sponsor visas.",
             {"Title": "Junior Python Developer", "CandidateCountry": ["USA", "Canada"], "VisaSponsorship": "no"}),
            ("Senior Data Engineer needed. You will work with Python, SQL, and Apache Airflow. Experience with dbt is a nice-to-have. No prior experience with AWS is required.",
             {"Title": "Senior Data Engineer", "Python": "required", "SQL": "required", "Apache_Airflow": "required",
              "dbt": "nice-to-have", "AWS": "no"}),
            ("Join us as a Frontend Developer. We offer 25 days of paid time off, health insurance, and a 5000 learning budget.",
             {"Title": "Frontend Developer", "PaidTimeOffDays": 25, "HealthInsurance": "yes",
              "LearningBudget": "5000"}),
            ("Senior DevOps Engineer role. Minimum 5 years of experience required. Master's degree preferred.",
             {"Title": "Senior DevOps Engineer", "MinYearsExperience": 5, "EducationLevel": "master"}),
            ("We are seeking a Machine Learning Engineer based in London, UK. The timezone is GMT. Salary ranges from 70,000 to 90,000 GBP annually. Relocation is offered with a 5000 budget.",
             {"Title": "Machine Learning Engineer", "EmployerCity": "London", "EmployerCountry": ["UK"],
              "EmployerTimezone": "GMT", "SalaryMin": "70000", "SalaryMax": "90000", "SalaryCurrency": "GBP",
              "SalaryPeriod": "year", "RelocationOffered": "yes", "RelocationBudget": "5000"}),
            ("Product Manager opening. The hiring process includes 3 interview rounds and a technical assessment. No coding challenge is required. We need to fill this role immediately.",
             {"Title": "Product Manager", "InterviewRounds": 3, "TechnicalAssessment": "yes", "CodingChallenge": "no",
              "Urgency": "immediate"}),
            ("Contract Software Engineer needed for a 12-month project. Probation period is 1 month. Notice period is 2 weeks. Working hours are 40 per week.",
             {"Title": "Contract Software Engineer", "ContractType": "contract", "ContractDurationMonths": 12,
              "ProbationPeriodMonths": 1, "NoticePeriodWeeks": 2, "WorkingHoursPerWeek": 40}),
            ("Join our startup as a Data Scientist. We are a team of 15 people reporting to the VP of Data. We are hiring 2 people for this role.",
             {"Title": "Data Scientist", "CompanyStage": "startup", "TeamSize": 15, "ReportingTo": "VP of Data",
              "NumberOfOpenPositions": 2}),
            ("We are looking for a Senior QA Engineer. Required languages: English, German. A background check is required, but no drug screening. An NDA is required, but no non-compete.",
             {"Title": "Senior QA Engineer", "RequiredLanguages": ["English", "German"], "BackgroundCheck": "yes",
              "DrugScreening": "no", "NDARequired": "yes", "NonCompeteRequired": "no"}),
            ("Data Engineer role posted on LinkedIn. Job ID is 123456789. Apply at https://careers.co/apply. Posted 4 days ago, over 100 applicants.",
             {"Title": "Data Engineer", "JobId": "123456789", "VacancySite": "LinkedIn",
              "ApplyURL": "https://careers.co/apply", "PublicationDate": "4 days ago", "ApplicantsCount": "Over 100"}),

            # 11-20
            ("DWH Developer needed. You will work with Star Schema, Snowflake Schema, and Data Vault. Experience with dbt and Apache Airflow is required. Knowledge of Kimball Methodology is a nice-to-have.",
             {"Title": "DWH Developer", "Star_Schema": "required", "Snowflake_Schema": "required",
              "Data_Vault": "required", "dbt": "required", "Apache_Airflow": "required",
              "Kimball_Methodology": "nice-to-have"}),
            ("Machine Learning Engineer. You will work with NLP, Computer Vision, and LLMs. Experience with PyTorch and TensorFlow is required. Familiarity with RAG and Prompt Engineering is a nice-to-have.",
             {"Title": "Machine Learning Engineer", "NLP": "required", "Computer_Vision": "required",
              "LLMs": "required", "PyTorch": "required", "TensorFlow": "required", "RAG": "nice-to-have",
              "Prompt_Engineering": "nice-to-have"}),
            ("DevOps Engineer. Required: Docker, Kubernetes, Terraform, Ansible. Nice-to-have: Jenkins, GitHub Actions. No experience with ArgoCD needed.",
             {"Title": "DevOps Engineer", "Docker": "required", "Kubernetes": "required", "Terraform": "required",
              "Ansible": "required", "Jenkins": "nice-to-have", "GitHub_Actions": "nice-to-have", "ArgoCD": "no"}),
            ("We are hiring a Senior Software Engineer. The role is fully remote, based in the USA. Salary is 120k-150k USD per year. We offer health insurance, 401k, and 20 days PTO. You need 5+ years of experience and a Bachelor's degree. The tech stack includes Python, SQL, and AWS.",
             {"Title": "Senior Software Engineer", "EmploymentType": "remote", "CandidateCountry": ["USA"],
              "SalaryMin": "120000", "SalaryMax": "150000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "HealthInsurance": "yes", "RetirementPlan": "yes", "PaidTimeOffDays": 20, "MinYearsExperience": 5,
              "EducationLevel": "bachelor", "Python": "required", "SQL": "required", "AWS": "required"}),
            ("Contract Data Analyst needed for a 6-month project. Probation is 1 month, notice period is 2 weeks. Working 40 hours/week. The company is a scale-up in the Financial Services industry. Team size is 10, reporting to the Head of Data. We are hiring 1 person. Minimum 3 years experience, Bachelor's degree required. Tech: SQL, Python, Tableau.",
             {"Title": "Contract Data Analyst", "ContractType": "contract", "ContractDurationMonths": 6,
              "ProbationPeriodMonths": 1, "NoticePeriodWeeks": 2, "WorkingHoursPerWeek": 40, "CompanyStage": "scale-up",
              "CompanyIndustry": "Financial Services", "TeamSize": 10, "ReportingTo": "Head of Data",
              "NumberOfOpenPositions": 1, "MinYearsExperience": 3, "EducationLevel": "bachelor", "SQL": "required",
              "Python": "required", "Tableau": "required"}),
            ("Backend Developer role. Required languages: English. Background check required, no drug screening, NDA required, no non-compete. Job ID: 987654. Posted on Indeed. Apply at https://apply.co. Posted 2 days ago, 50 applicants. Tech: Java, Spring Boot, PostgreSQL.",
             {"Title": "Backend Developer", "RequiredLanguages": ["English"], "BackgroundCheck": "yes",
              "DrugScreening": "no", "NDARequired": "yes", "NonCompeteRequired": "no", "JobId": "987654",
              "VacancySite": "Indeed", "ApplyURL": "https://apply.co", "PublicationDate": "2 days ago",
              "ApplicantsCount": "50", "Java": "required", "Spring_Boot": "required", "PostgreSQL": "required"}),
            ("AI Research Scientist. You will work with Deep Learning, Neural Networks, NLP, and LLMs. Experience with PyTorch, TensorFlow, and RAG is required. Nice-to-have: Prompt Engineering, Fine-Tuning. Soft skills: Communication, Teamwork, Problem Solving, Critical Thinking.",
             {"Title": "AI Research Scientist", "Deep_Learning": "required", "Neural_Networks": "required",
              "NLP": "required", "LLMs": "required", "PyTorch": "required", "TensorFlow": "required", "RAG": "required",
              "Prompt_Engineering": "nice-to-have", "Fine_Tuning": "nice-to-have", "Communication": "required",
              "Teamwork": "required", "Problem_Solving": "required", "Critical_Thinking": "required"}),
            ("Full Stack Data Warehouse Developer. Remote, USA. Salary 100k-130k USD/year. Health insurance, 401k, 25 days PTO, 5000 learning budget. 5+ years experience, Bachelor's degree. Tech: Python, SQL, dbt, Apache Airflow, Star Schema, Snowflake Schema. 3 interview rounds, technical assessment, no coding challenge. Urgency: within-1-month.",
             {"Title": "Full Stack Data Warehouse Developer", "EmploymentType": "remote", "CandidateCountry": ["USA"],
              "SalaryMin": "100000", "SalaryMax": "130000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "HealthInsurance": "yes", "RetirementPlan": "yes", "PaidTimeOffDays": 25, "LearningBudget": "5000",
              "MinYearsExperience": 5, "EducationLevel": "bachelor", "Python": "required", "SQL": "required",
              "dbt": "required", "Apache_Airflow": "required", "Star_Schema": "required",
              "Snowflake_Schema": "required", "InterviewRounds": 3, "TechnicalAssessment": "yes",
              "CodingChallenge": "no", "Urgency": "within-1-month"}),
            ("We are hiring a Frontend Developer. Location: remote, USA. Salary: 80000-110000 USD per year. Benefits include: Health insurance, 20 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 3 years. Tech stack: React, TypeScript, CSS, HTML, Webpack, Vite. Soft skills: Communication, Teamwork, Adaptability.",
             {"Title": "Frontend Developer", "EmploymentType": "remote", "CandidateCountry": ["USA"],
              "SalaryMin": "80000", "SalaryMax": "110000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "React": "required", "TypeScript": "required", "CSS": "required", "HTML": "required",
              "Webpack": "required", "Vite": "required", "Communication": "required", "Teamwork": "required",
              "Adaptability": "required"}),
            ("We are hiring a Data Engineer. Location: hybrid, UK. Salary: 90000-120000 GBP per year. Benefits include: 401k, learning budget 2000. Hiring process: 4 rounds, no coding challenge. Requirements: Master's, 5 years. Tech stack: Python, SQL, Spark, Kafka, AWS, dbt. Soft skills: Problem Solving, Critical Thinking.",
             {"Title": "Data Engineer", "EmploymentType": "hybrid", "CandidateCountry": ["UK"], "SalaryMin": "90000",
              "SalaryMax": "120000", "SalaryCurrency": "GBP", "SalaryPeriod": "year", "Python": "required",
              "SQL": "required", "Spark": "required", "Kafka": "required", "AWS": "required", "dbt": "required",
              "Problem_Solving": "required", "Critical_Thinking": "required"}),

            # 21-30
            ("We are hiring a DevOps Engineer. Location: remote, Canada. Salary: 100000-140000 CAD per year. Benefits include: Stock options, unlimited PTO. Hiring process: 2 rounds, system design. Requirements: Bachelor's, 4 years. Tech stack: Docker, Kubernetes, Terraform, Ansible, Jenkins. Soft skills: Leadership, Time Management.",
             {"Title": "DevOps Engineer", "EmploymentType": "remote", "CandidateCountry": ["Canada"],
              "SalaryMin": "100000", "SalaryMax": "140000", "SalaryCurrency": "CAD", "SalaryPeriod": "year",
              "Docker": "required", "Kubernetes": "required", "Terraform": "required", "Ansible": "required",
              "Jenkins": "required", "Leadership": "required", "Time_Management": "required"}),
            ("We are hiring a Product Manager. Location: office, Germany. Salary: 70000-95000 EUR per year. Benefits include: Health, dental, 15 days PTO. Hiring process: 3 rounds, case study. Requirements: Bachelor's, 6 years. Tech stack: Jira, Confluence, Figma, SQL. Soft skills: Negotiation, Empathy, Decision Making.",
             {"Title": "Product Manager", "EmploymentType": "office", "CandidateCountry": ["Germany"],
              "SalaryMin": "70000", "SalaryMax": "95000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Jira": "required", "Confluence": "required", "Figma": "required", "SQL": "required",
              "Negotiation": "required", "Empathy": "required", "Decision_Making": "required"}),
            ("We are hiring a QA Automation Engineer. Location: remote, Australia. Salary: 85000-105000 AUD per year. Benefits include: Gym membership, 22 days PTO. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: Python, Selenium, PyTest, Jenkins, Docker. Soft skills: Attention to Detail, Patience.",
             {"Title": "QA Automation Engineer", "EmploymentType": "remote", "CandidateCountry": ["Australia"],
              "SalaryMin": "85000", "SalaryMax": "105000", "SalaryCurrency": "AUD", "SalaryPeriod": "year",
              "Python": "required", "Selenium": "required", "PyTest": "required", "Jenkins": "required",
              "Docker": "required", "Attention_to_Detail": "required", "Patience": "required"}),
            ("We are hiring a Machine Learning Engineer. Location: hybrid, France. Salary: 60000-85000 EUR per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 4 rounds, technical assessment. Requirements: PhD, 2 years. Tech stack: Python, PyTorch, TensorFlow, NLP, LLMs. Soft skills: Creativity, Analytical Thinking.",
             {"Title": "Machine Learning Engineer", "EmploymentType": "hybrid", "CandidateCountry": ["France"],
              "SalaryMin": "60000", "SalaryMax": "85000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Python": "required", "PyTorch": "required", "TensorFlow": "required", "NLP": "required",
              "LLMs": "required", "Creativity": "required", "Analytical_Thinking": "required"}),
            ("We are hiring a Backend Developer. Location: remote, Netherlands. Salary: 75000-95000 EUR per year. Benefits include: Meal allowance, 20 days PTO. Hiring process: 3 rounds, take-home assignment. Requirements: Bachelor's, 4 years. Tech stack: Java, Spring Boot, PostgreSQL, Redis, Kafka. Soft skills: Collaboration, Work Ethic.",
             {"Title": "Backend Developer", "EmploymentType": "remote", "CandidateCountry": ["Netherlands"],
              "SalaryMin": "75000", "SalaryMax": "95000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Java": "required", "Spring_Boot": "required", "PostgreSQL": "required", "Redis": "required",
              "Kafka": "required", "Collaboration": "required", "Work_Ethic": "required"}),
            ("We are hiring a UI/UX Designer. Location: hybrid, Spain. Salary: 50000-70000 EUR per year. Benefits include: Health, 18 days PTO, learning budget. Hiring process: 3 rounds, portfolio review. Requirements: Bachelor's, 3 years. Tech stack: Figma, Sketch, Adobe XD, User Research. Soft skills: Empathy, Communication, Creativity.",
             {"Title": "UI/UX Designer", "EmploymentType": "hybrid", "CandidateCountry": ["Spain"],
              "SalaryMin": "50000", "SalaryMax": "70000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Figma": "required", "Sketch": "required", "Adobe_XD": "required", "User_Research": "required",
              "Empathy": "required", "Communication": "required", "Creativity": "required"}),
            ("We are hiring a Cloud Architect. Location: remote, USA. Salary: 150000-200000 USD per year. Benefits include: Stock options, 30 days PTO. Hiring process: 4 rounds, architecture review. Requirements: Master's, 8 years. Tech stack: AWS, Azure, GCP, Terraform, Kubernetes. Soft skills: Strategic Thinking, Leadership.",
             {"Title": "Cloud Architect", "EmploymentType": "remote", "CandidateCountry": ["USA"],
              "SalaryMin": "150000", "SalaryMax": "200000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "AWS": "required", "Azure": "required", "GCP": "required", "Terraform": "required",
              "Kubernetes": "required", "Strategic_Thinking": "required", "Leadership": "required"}),
            ("We are hiring a Security Engineer. Location: office, UK. Salary: 90000-120000 GBP per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 5 years. Tech stack: Python, Bash, Linux, Wireshark, Splunk. Soft skills: Critical Thinking, Attention to Detail.",
             {"Title": "Security Engineer", "EmploymentType": "office", "CandidateCountry": ["UK"],
              "SalaryMin": "90000", "SalaryMax": "120000", "SalaryCurrency": "GBP", "SalaryPeriod": "year",
              "Python": "required", "Bash": "required", "Linux": "required", "Wireshark": "required",
              "Splunk": "required", "Critical_Thinking": "required", "Attention_to_Detail": "required"}),
            ("We are hiring a Mobile Developer. Location: remote, Canada. Salary: 80000-110000 CAD per year. Benefits include: Health, 20 days PTO, gym. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: Swift, Kotlin, React Native, Firebase. Soft skills: Adaptability, Problem Solving.",
             {"Title": "Mobile Developer", "EmploymentType": "remote", "CandidateCountry": ["Canada"],
              "SalaryMin": "80000", "SalaryMax": "110000", "SalaryCurrency": "CAD", "SalaryPeriod": "year",
              "Swift": "required", "Kotlin": "required", "React_Native": "required", "Firebase": "required",
              "Adaptability": "required", "Problem_Solving": "required"}),
            ("We are hiring a Site Reliability Engineer. Location: hybrid, Germany. Salary: 85000-115000 EUR per year. Benefits include: Unlimited PTO, stock options. Hiring process: 3 rounds, system design. Requirements: Bachelor's, 4 years. Tech stack: Go, Python, Kubernetes, Prometheus, Grafana. Soft skills: Stress Management, Teamwork.",
             {"Title": "Site Reliability Engineer", "EmploymentType": "hybrid", "CandidateCountry": ["Germany"],
              "SalaryMin": "85000", "SalaryMax": "115000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Go": "required", "Python": "required", "Kubernetes": "required", "Prometheus": "required",
              "Grafana": "required", "Stress_Management": "required", "Teamwork": "required"}),

            # 31-40
            ("We are hiring a Business Analyst. Location: office, Australia. Salary: 70000-90000 AUD per year. Benefits include: Health, 22 days PTO. Hiring process: 2 rounds, case study. Requirements: Bachelor's, 2 years. Tech stack: SQL, Excel, Tableau, Power BI. Soft skills: Communication, Analytical Thinking.",
             {"Title": "Business Analyst", "EmploymentType": "office", "CandidateCountry": ["Australia"],
              "SalaryMin": "70000", "SalaryMax": "90000", "SalaryCurrency": "AUD", "SalaryPeriod": "year",
              "SQL": "required", "Excel": "required", "Tableau": "required", "Power_BI": "required",
              "Communication": "required", "Analytical_Thinking": "required"}),
            ("We are hiring a Network Engineer. Location: remote, France. Salary: 65000-85000 EUR per year. Benefits include: Health, 20 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 5 years. Tech stack: Cisco, Juniper, Python, BGP, OSPF. Soft skills: Problem Solving, Attention to Detail.",
             {"Title": "Network Engineer", "EmploymentType": "remote", "CandidateCountry": ["France"],
              "SalaryMin": "65000", "SalaryMax": "85000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Cisco": "required", "Juniper": "required", "Python": "required", "BGP": "required", "OSPF": "required",
              "Problem_Solving": "required", "Attention_to_Detail": "required"}),
            ("We are hiring a Scrum Master. Location: hybrid, Netherlands. Salary: 70000-90000 EUR per year. Benefits include: Health, 25 days PTO, learning budget. Hiring process: 2 rounds, behavioral. Requirements: Bachelor's, 4 years. Tech stack: Jira, Confluence, Agile, Scrum. Soft skills: Leadership, Empathy, Communication.",
             {"Title": "Scrum Master", "EmploymentType": "hybrid", "CandidateCountry": ["Netherlands"],
              "SalaryMin": "70000", "SalaryMax": "90000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Jira": "required", "Confluence": "required", "Agile": "required", "Scrum": "required",
              "Leadership": "required", "Empathy": "required", "Communication": "required"}),
            ("We are hiring a Database Administrator. Location: office, Spain. Salary: 60000-80000 EUR per year. Benefits include: Health, 401k, 20 days PTO. Hiring process: 3 rounds, technical assessment. Requirements: Bachelor's, 5 years. Tech stack: PostgreSQL, MySQL, Oracle, SQL Server. Soft skills: Attention to Detail, Problem Solving.",
             {"Title": "Database Administrator", "EmploymentType": "office", "CandidateCountry": ["Spain"],
              "SalaryMin": "60000", "SalaryMax": "80000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "PostgreSQL": "required", "MySQL": "required", "Oracle": "required", "SQL_Server": "required",
              "Attention_to_Detail": "required", "Problem_Solving": "required"}),
            ("We are hiring a Technical Writer. Location: remote, USA. Salary: 70000-90000 USD per year. Benefits include: Health, 20 days PTO, remote work. Hiring process: 2 rounds, writing test. Requirements: Bachelor's, 2 years. Tech stack: Markdown, Git, Confluence, Jira. Soft skills: Written Communication, Attention to Detail.",
             {"Title": "Technical Writer", "EmploymentType": "remote", "CandidateCountry": ["USA"],
              "SalaryMin": "70000", "SalaryMax": "90000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "Markdown": "required", "Git": "required", "Confluence": "required", "Jira": "required",
              "Written_Communication": "required", "Attention_to_Detail": "required"}),
            ("We are hiring a Game Developer. Location: office, UK. Salary: 60000-85000 GBP per year. Benefits include: Health, 20 days PTO, game allowance. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: C++, Unreal Engine, Unity, C#. Soft skills: Creativity, Teamwork, Problem Solving.",
             {"Title": "Game Developer", "EmploymentType": "office", "CandidateCountry": ["UK"], "SalaryMin": "60000",
              "SalaryMax": "85000", "SalaryCurrency": "GBP", "SalaryPeriod": "year", "C_Plus_Plus": "required",
              "Unreal_Engine": "required", "Unity": "required", "C_Sharp": "required", "Creativity": "required",
              "Teamwork": "required", "Problem_Solving": "required"}),
            ("We are hiring a Systems Administrator. Location: hybrid, Canada. Salary: 75000-95000 CAD per year. Benefits include: Health, 22 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 4 years. Tech stack: Linux, Windows, Bash, PowerShell, Ansible. Soft skills: Problem Solving, Time Management.",
             {"Title": "Systems Administrator", "EmploymentType": "hybrid", "CandidateCountry": ["Canada"],
              "SalaryMin": "75000", "SalaryMax": "95000", "SalaryCurrency": "CAD", "SalaryPeriod": "year",
              "Linux": "required", "Windows": "required", "Bash": "required", "PowerShell": "required",
              "Ansible": "required", "Problem_Solving": "required", "Time_Management": "required"}),
            ("We are hiring a Data Scientist. Location: remote, Germany. Salary: 80000-110000 EUR per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 4 rounds, technical assessment. Requirements: Master's, 3 years. Tech stack: Python, R, SQL, Machine Learning, Pandas. Soft skills: Analytical Thinking, Communication.",
             {"Title": "Data Scientist", "EmploymentType": "remote", "CandidateCountry": ["Germany"],
              "SalaryMin": "80000", "SalaryMax": "110000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Python": "required", "R": "required", "SQL": "required", "Machine_Learning": "required",
              "Pandas": "required", "Analytical_Thinking": "required", "Communication": "required"}),
            ("We are hiring a Frontend Architect. Location: remote, USA. Salary: 160000-210000 USD per year. Benefits include: Stock options, 30 days PTO. Hiring process: 4 rounds, architecture review. Requirements: Master's, 8 years. Tech stack: React, TypeScript, Node.js, GraphQL, AWS. Soft skills: Leadership, Strategic Thinking.",
             {"Title": "Frontend Architect", "EmploymentType": "remote", "CandidateCountry": ["USA"],
              "SalaryMin": "160000", "SalaryMax": "210000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "React": "required", "TypeScript": "required", "Node_js": "required", "GraphQL": "required",
              "AWS": "required", "Leadership": "required", "Strategic_Thinking": "required"}),
            ("We are hiring an Embedded Systems Engineer. Location: office, UK. Salary: 70000-95000 GBP per year. Benefits include: Health, 20 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 5 years. Tech stack: C, C++, RTOS, ARM, Linux. Soft skills: Attention to Detail, Problem Solving.",
             {"Title": "Embedded Systems Engineer", "EmploymentType": "office", "CandidateCountry": ["UK"],
              "SalaryMin": "70000", "SalaryMax": "95000", "SalaryCurrency": "GBP", "SalaryPeriod": "year",
              "C": "required", "C_Plus_Plus": "required", "RTOS": "required", "ARM": "required", "Linux": "required",
              "Attention_to_Detail": "required", "Problem_Solving": "required"}),

            # 41-50
            ("We are hiring an IT Support Specialist. Location: office, Australia. Salary: 50000-65000 AUD per year. Benefits include: Health, 15 days PTO. Hiring process: 2 rounds, practical test. Requirements: High-school, 1 year. Tech stack: Windows, macOS, Active Directory, Office 365. Soft skills: Customer Service, Patience.",
             {"Title": "IT Support Specialist", "EmploymentType": "office", "CandidateCountry": ["Australia"],
              "SalaryMin": "50000", "SalaryMax": "65000", "SalaryCurrency": "AUD", "SalaryPeriod": "year",
              "Windows": "required", "macOS": "required", "Active_Directory": "required", "Office_365": "required",
              "Customer_Service": "required", "Patience": "required"}),
            ("We are hiring a Blockchain Developer. Location: remote, Switzerland. Salary: 100000-150000 CHF per year. Benefits include: Crypto bonuses, 25 days PTO. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 3 years. Tech stack: Solidity, Rust, Ethereum, Web3, Smart Contracts. Soft skills: Analytical Thinking, Problem Solving.",
             {"Title": "Blockchain Developer", "EmploymentType": "remote", "CandidateCountry": ["Switzerland"],
              "SalaryMin": "100000", "SalaryMax": "150000", "SalaryCurrency": "CHF", "SalaryPeriod": "year",
              "Solidity": "required", "Rust": "required", "Ethereum": "required", "Web3": "required",
              "Smart_Contracts": "required", "Analytical_Thinking": "required", "Problem_Solving": "required"}),
            ("We are hiring a Growth Hacker. Location: hybrid, Netherlands. Salary: 65000-85000 EUR per year. Benefits include: Health, 20 days PTO, performance bonus. Hiring process: 3 rounds, case study. Requirements: Bachelor's, 3 years. Tech stack: SQL, Python, Google Analytics, A/B Testing. Soft skills: Creativity, Analytical Thinking.",
             {"Title": "Growth Hacker", "EmploymentType": "hybrid", "CandidateCountry": ["Netherlands"],
              "SalaryMin": "65000", "SalaryMax": "85000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "SQL": "required", "Python": "required", "Google_Analytics": "required", "A_B_Testing": "required",
              "Creativity": "required", "Analytical_Thinking": "required"}),
            ("We are hiring a Solutions Architect. Location: remote, USA. Salary: 140000-190000 USD per year. Benefits include: Stock options, 30 days PTO. Hiring process: 4 rounds, architecture review. Requirements: Master's, 7 years. Tech stack: AWS, Azure, GCP, Terraform, Microservices. Soft skills: Strategic Thinking, Communication.",
             {"Title": "Solutions Architect", "EmploymentType": "remote", "CandidateCountry": ["USA"],
              "SalaryMin": "140000", "SalaryMax": "190000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "AWS": "required", "Azure": "required", "GCP": "required", "Terraform": "required",
              "Microservices": "required", "Strategic_Thinking": "required", "Communication": "required"}),
            ("We are hiring a Quality Assurance Lead. Location: hybrid, UK. Salary: 80000-110000 GBP per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 3 rounds, technical assessment. Requirements: Bachelor's, 6 years. Tech stack: Python, Selenium, Cypress, Jenkins, Jira. Soft skills: Leadership, Attention to Detail.",
             {"Title": "Quality Assurance Lead", "EmploymentType": "hybrid", "CandidateCountry": ["UK"],
              "SalaryMin": "80000", "SalaryMax": "110000", "SalaryCurrency": "GBP", "SalaryPeriod": "year",
              "Python": "required", "Selenium": "required", "Cypress": "required", "Jenkins": "required",
              "Jira": "required", "Leadership": "required", "Attention_to_Detail": "required"}),
            ("We are hiring a Full Stack Engineer. Location: remote, Canada. Salary: 90000-120000 CAD per year. Benefits include: Health, 20 days PTO, learning budget. Hiring process: 3 rounds, coding challenge. Requirements: Bachelor's, 4 years. Tech stack: JavaScript, TypeScript, React, Node.js, PostgreSQL. Soft skills: Teamwork, Problem Solving.",
             {"Title": "Full Stack Engineer", "EmploymentType": "remote", "CandidateCountry": ["Canada"],
              "SalaryMin": "90000", "SalaryMax": "120000", "SalaryCurrency": "CAD", "SalaryPeriod": "year",
              "JavaScript": "required", "TypeScript": "required", "React": "required", "Node_js": "required",
              "PostgreSQL": "required", "Teamwork": "required", "Problem_Solving": "required"}),
            ("We are hiring a Machine Learning Ops Engineer. Location: remote, Germany. Salary: 85000-115000 EUR per year. Benefits include: Health, 401k, 25 days PTO. Hiring process: 3 rounds, technical test. Requirements: Bachelor's, 4 years. Tech stack: Python, Docker, Kubernetes, MLflow, AWS. Soft skills: Problem Solving, Automation.",
             {"Title": "Machine Learning Ops Engineer", "EmploymentType": "remote", "CandidateCountry": ["Germany"],
              "SalaryMin": "85000", "SalaryMax": "115000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "Python": "required", "Docker": "required", "Kubernetes": "required", "MLflow": "required",
              "AWS": "required", "Problem_Solving": "required", "Automation": "required"}),
            ("We are hiring a Chief Technology Officer. Location: hybrid, USA. Salary: 200000-300000 USD per year. Benefits include: Equity, 40 days PTO, executive benefits. Hiring process: 3 rounds, executive interview. Requirements: Master's, 15 years. Tech stack: Strategic Planning, Team Leadership, Architecture. Soft skills: Leadership, Strategic Thinking, Vision.",
             {"Title": "Chief Technology Officer", "EmploymentType": "hybrid", "CandidateCountry": ["USA"],
              "SalaryMin": "200000", "SalaryMax": "300000", "SalaryCurrency": "USD", "SalaryPeriod": "year",
              "Strategic_Planning": "required", "Team_Leadership": "required", "Architecture": "required",
              "Leadership": "required", "Strategic_Thinking": "required", "Vision": "required"}),
            ("We are hiring a Cybersecurity Analyst. Location: office, Canada. Salary: 75000-95000 CAD per year. Benefits include: Health, 20 days PTO, certification budget. Hiring process: 3 rounds, technical assessment. Requirements: Bachelor's, 3 years. Tech stack: SIEM, Wireshark, Python, Linux, Firewall Management. Soft skills: Analytical Thinking, Attention to Detail.",
             {"Title": "Cybersecurity Analyst", "EmploymentType": "office", "CandidateCountry": ["Canada"],
              "SalaryMin": "75000", "SalaryMax": "95000", "SalaryCurrency": "CAD", "SalaryPeriod": "year",
              "SIEM": "required", "Wireshark": "required", "Python": "required", "Linux": "required",
              "Firewall_Management": "required", "Analytical_Thinking": "required", "Attention_to_Detail": "required"}),
            ("We are hiring a Robotics Engineer. Location: hybrid, Germany. Salary: 80000-110000 EUR per year. Benefits include: Health, 25 days PTO, relocation support. Hiring process: 4 rounds, practical test. Requirements: Master's, 5 years. Tech stack: C++, ROS, Python, MATLAB, Computer Vision. Soft skills: Problem Solving, Innovation, Teamwork.",
             {"Title": "Robotics Engineer", "EmploymentType": "hybrid", "CandidateCountry": ["Germany"],
              "SalaryMin": "80000", "SalaryMax": "110000", "SalaryCurrency": "EUR", "SalaryPeriod": "year",
              "C_Plus_Plus": "required", "ROS": "required", "Python": "required", "MATLAB": "required",
              "Computer_Vision": "required", "Problem_Solving": "required", "Innovation": "required",
              "Teamwork": "required"})
        ]

        questions = []
        for idx, (vacancy_text, real_expected) in enumerate(real_data):
            keys = list(real_expected.keys())
            keys_str = ", ".join([f'"{k}"' for k in keys])

            # Create a dummy example format with placeholder values to prevent the model from just copying the answer
            example_format = {}
            for k in keys:
                if isinstance(real_expected[k], list):
                    example_format[k] = ["Example"]
                elif isinstance(real_expected[k], (int, float)):
                    example_format[k] = 999
                else:
                    example_format[k] = "Example Value"

            prompt = (
                f"====TEXT of VACANCY====\n{vacancy_text}\n====END TEXT====\n\n"
                f"ROLE & TASK: You are an expert technical recruiter and data extraction AI. Analyze the job description and extract specific details.\n"
                f"Extract the following details and return ONLY a valid JSON object with these exact keys: {keys_str}. "
                f"Do not add any markdown formatting, extra text, or explanations. Do not wrap the JSON in markdown code blocks (no ```json). "
                f"Example JSON format (values are examples, extract the ACTUAL values from the text): {json.dumps(example_format)}"
            )

            questions.append({
                "question": prompt,
                "expected_json": real_expected,
                "summary": f"Extract details from vacancy {idx + 1}."
            })

        return questions