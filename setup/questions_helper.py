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
        questions = [
            # 1-10: Short (3-5 lines), simple subjects
            {
                "question": "====TEXT of VACANCY====\nWe are hiring a Junior Python Developer. The role is fully remote. You must be located in the USA or Canada. We do not sponsor visas.\n====END TEXT====\n\nExtract: Title, CandidateCountry, VisaSponsorship. Example: {\"Title\": \"Role\", \"CandidateCountry\": [\"USA\"], \"VisaSponsorship\": \"no\"}",
                "expected_json": {"Title": "Junior Python Developer", "CandidateCountry": ["USA", "Canada"],
                                  "VisaSponsorship": "no"},
                "summary": "Extract title, country, visa from short vacancy 1."
            },
            {
                "question": "====TEXT of VACANCY====\nLooking for a Data Analyst. Salary is 40k to 60k EUR per year. This is a full-time position.\n====END TEXT====\n\nExtract: Title, SalaryMin, SalaryMax, SalaryCurrency, SalaryPeriod, FullTime. Example: {\"Title\": \"Role\", \"SalaryMin\": \"50000\", \"SalaryMax\": \"75000\", \"SalaryCurrency\": \"USD\", \"SalaryPeriod\": \"year\", \"FullTime\": \"yes\"}",
                "expected_json": {"Title": "Data Analyst", "SalaryMin": "40000", "SalaryMax": "60000",
                                  "SalaryCurrency": "EUR", "SalaryPeriod": "year", "FullTime": "yes"},
                "summary": "Extract title, salary, fulltime from short vacancy 2."
            },
            {
                "question": "====TEXT of VACANCY====\nBackend Engineer needed. You must have expert level Python and required level SQL. Nice-to-have knowledge of Docker.\n====END TEXT====\n\nExtract: Title, Python, SQL, Docker. Example: {\"Title\": \"Role\", \"Python\": \"expert\", \"SQL\": \"required\", \"Docker\": \"nice-to-have\"}",
                "expected_json": {"Title": "Backend Engineer", "Python": "expert", "SQL": "required",
                                  "Docker": "nice-to-have"},
                "summary": "Extract title and tech proficiency from short vacancy 3."
            },
            {
                "question": "====TEXT of VACANCY====\nJoin us as a Frontend Developer. We offer 25 days of paid time off, health insurance, and a 5000 learning budget.\n====END TEXT====\n\nExtract: Title, PaidTimeOffDays, HealthInsurance, LearningBudget. Example: {\"Title\": \"Role\", \"PaidTimeOffDays\": 20, \"HealthInsurance\": \"yes\", \"LearningBudget\": \"1000\"}",
                "expected_json": {"Title": "Frontend Developer", "PaidTimeOffDays": 25, "HealthInsurance": "yes",
                                  "LearningBudget": "5000"},
                "summary": "Extract title and benefits from short vacancy 4."
            },
            {
                "question": "====TEXT of VACANCY====\nSenior DevOps Engineer role. Minimum 5 years of experience required. Master's degree preferred.\n====END TEXT====\n\nExtract: Title, MinYearsExperience, EducationLevel. Example: {\"Title\": \"Role\", \"MinYearsExperience\": 3, \"EducationLevel\": \"bachelor\"}",
                "expected_json": {"Title": "Senior DevOps Engineer", "MinYearsExperience": 5,
                                  "EducationLevel": "master"},
                "summary": "Extract title, experience, education from short vacancy 5."
            },
            {
                "question": "====TEXT of VACANCY====\nWe are seeking a Machine Learning Engineer based in London, UK. The timezone is GMT. Salary ranges from 70,000 to 90,000 GBP annually. Relocation is offered with a 5000 budget.\n====END TEXT====\n\nExtract: Title, EmployerCity, EmployerCountry, EmployerTimezone, SalaryMin, SalaryMax, SalaryCurrency, SalaryPeriod, RelocationOffered, RelocationBudget. Example: {\"Title\": \"Role\", \"EmployerCity\": \"City\", \"EmployerCountry\": [\"USA\"], \"EmployerTimezone\": \"EST\", \"SalaryMin\": \"50000\", \"SalaryMax\": \"75000\", \"SalaryCurrency\": \"USD\", \"SalaryPeriod\": \"year\", \"RelocationOffered\": \"yes\", \"RelocationBudget\": \"1000\"}",
                "expected_json": {"Title": "Machine Learning Engineer", "EmployerCity": "London",
                                  "EmployerCountry": ["UK"], "EmployerTimezone": "GMT", "SalaryMin": "70000",
                                  "SalaryMax": "90000", "SalaryCurrency": "GBP", "SalaryPeriod": "year",
                                  "RelocationOffered": "yes", "RelocationBudget": "5000"},
                "summary": "Extract location, salary, relocation from medium vacancy 6."
            },
            {
                "question": "====TEXT of VACANCY====\nFull Stack Developer position. Required skills: JavaScript, TypeScript, React, Node.js. Experience with PostgreSQL is a must. Familiarity with AWS is a nice-to-have. No prior experience with Azure needed.\n====END TEXT====\n\nExtract: Title, JavaScript, TypeScript, React, Node.js, PostgreSQL, AWS, Azure. Example: {\"Title\": \"Role\", \"JavaScript\": \"required\", \"TypeScript\": \"required\", \"React\": \"required\", \"Node.js\": \"required\", \"PostgreSQL\": \"required\", \"AWS\": \"nice-to-have\", \"Azure\": \"no\"}",
                "expected_json": {"Title": "Full Stack Developer", "JavaScript": "required", "TypeScript": "required",
                                  "React": "required", "Node.js": "required", "PostgreSQL": "required",
                                  "AWS": "nice-to-have", "Azure": "no"},
                "summary": "Extract tech stack proficiencies from medium vacancy 7."
            },
            {
                "question": "====TEXT of VACANCY====\nProduct Manager opening. The hiring process includes 3 interview rounds and a technical assessment. No coding challenge is required. We need to fill this role immediately.\n====END TEXT====\n\nExtract: Title, InterviewRounds, TechnicalAssessment, CodingChallenge, Urgency. Example: {\"Title\": \"Role\", \"InterviewRounds\": 2, \"TechnicalAssessment\": \"yes\", \"CodingChallenge\": \"yes\", \"Urgency\": \"flexible\"}",
                "expected_json": {"Title": "Product Manager", "InterviewRounds": 3, "TechnicalAssessment": "yes",
                                  "CodingChallenge": "no", "Urgency": "immediate"},
                "summary": "Extract hiring process details from medium vacancy 8."
            },
            {
                "question": "====TEXT of VACANCY====\nContract Software Engineer needed for a 12-month project. Probation period is 1 month. Notice period is 2 weeks. Working hours are 40 per week.\n====END TEXT====\n\nExtract: Title, ContractType, ContractDurationMonths, ProbationPeriodMonths, NoticePeriodWeeks, WorkingHoursPerWeek. Example: {\"Title\": \"Role\", \"ContractType\": \"permanent\", \"ContractDurationMonths\": 6, \"ProbationPeriodMonths\": 3, \"NoticePeriodWeeks\": 4, \"WorkingHoursPerWeek\": 37.5}",
                "expected_json": {"Title": "Contract Software Engineer", "ContractType": "contract",
                                  "ContractDurationMonths": 12, "ProbationPeriodMonths": 1, "NoticePeriodWeeks": 2,
                                  "WorkingHoursPerWeek": 40},
                "summary": "Extract contract details from medium vacancy 9."
            },
            {
                "question": "====TEXT of VACANCY====\nJoin our startup as a Data Scientist. We are a team of 15 people reporting to the VP of Data. We are hiring 2 people for this role.\n====END TEXT====\n\nExtract: Title, CompanyStage, TeamSize, ReportingTo, NumberOfOpenPositions. Example: {\"Title\": \"Role\", \"CompanyStage\": \"enterprise\", \"TeamSize\": 50, \"ReportingTo\": \"Manager\", \"NumberOfOpenPositions\": 1}",
                "expected_json": {"Title": "Data Scientist", "CompanyStage": "startup", "TeamSize": 15,
                                  "ReportingTo": "VP of Data", "NumberOfOpenPositions": 2},
                "summary": "Extract company and team info from medium vacancy 10."
            },
            # 11-20: Medium (6-10 lines), varied subjects
            {
                "question": "====TEXT of VACANCY====\nWe are looking for a Senior QA Engineer. Required languages: English, German. A background check is required, but no drug screening. An NDA is required, but no non-compete.\n====END TEXT====\n\nExtract: Title, RequiredLanguages, BackgroundCheck, DrugScreening, NDARequired, NonCompeteRequired. Example: {\"Title\": \"Role\", \"RequiredLanguages\": [\"English\"], \"BackgroundCheck\": \"no\", \"DrugScreening\": \"yes\", \"NDARequired\": \"no\", \"NonCompeteRequired\": \"yes\"}",
                "expected_json": {"Title": "Senior QA Engineer", "RequiredLanguages": ["English", "German"],
                                  "BackgroundCheck": "yes", "DrugScreening": "no", "NDARequired": "yes",
                                  "NonCompeteRequired": "no"},
                "summary": "Extract work conditions from medium vacancy 11."
            },
            {
                "question": "====TEXT of VACANCY====\nData Engineer role posted on LinkedIn. Job ID is 123456789. Apply at https://careers.co/apply. Posted 4 days ago, over 100 applicants.\n====END TEXT====\n\nExtract: Title, JobId, VacancySite, ApplyURL, PublicationDate, ApplicantsCount. Example: {\"Title\": \"Role\", \"JobId\": \"000\", \"VacancySite\": \"Indeed\", \"ApplyURL\": \"url\", \"PublicationDate\": \"1 day ago\", \"ApplicantsCount\": \"50\"}",
                "expected_json": {"Title": "Data Engineer", "JobId": "123456789", "VacancySite": "LinkedIn",
                                  "ApplyURL": "https://careers.co/", "PublicationDate": "4 days ago",
                                  "ApplicantsCount": "Over 100"},
                "summary": "Extract metadata from medium vacancy 12."
            },
            {
                "question": "====TEXT of VACANCY====\nDWH Developer needed. You will work with Star Schema, Snowflake Schema, and Data Vault. Experience with dbt and Apache Airflow is required. Knowledge of Kimball Methodology is a nice-to-have.\n====END TEXT====\n\nExtract: Title, Star_Schema, Snowflake_Schema, Data_Vault, dbt, Apache_Airflow, Kimball_Methodology. Example: {\"Title\": \"Role\", \"Star_Schema\": \"required\", \"Snowflake_Schema\": \"no\", \"Data_Vault\": \"no\", \"dbt\": \"no\", \"Apache_Airflow\": \"no\", \"Kimball_Methodology\": \"no\"}",
                "expected_json": {"Title": "DWH Developer", "Star_Schema": "required", "Snowflake_Schema": "required",
                                  "Data_Vault": "required", "dbt": "required", "Apache_Airflow": "required",
                                  "Kimball_Methodology": "nice-to-have"},
                "summary": "Extract DWH concepts from medium vacancy 13."
            },
            {
                "question": "====TEXT of VACANCY====\nMachine Learning Engineer. You will work with NLP, Computer Vision, and LLMs. Experience with PyTorch and TensorFlow is required. Familiarity with RAG and Prompt Engineering is a nice-to-have.\n====END TEXT====\n\nExtract: Title, NLP, Computer_Vision, LLMs, PyTorch, TensorFlow, RAG, Prompt_Engineering. Example: {\"Title\": \"Role\", \"NLP\": \"no\", \"Computer_Vision\": \"no\", \"LLMs\": \"no\", \"PyTorch\": \"no\", \"TensorFlow\": \"no\", \"RAG\": \"no\", \"Prompt_Engineering\": \"no\"}",
                "expected_json": {"Title": "Machine Learning Engineer", "NLP": "required",
                                  "Computer_Vision": "required", "LLMs": "required", "PyTorch": "required",
                                  "TensorFlow": "required", "RAG": "nice-to-have",
                                  "Prompt_Engineering": "nice-to-have"},
                "summary": "Extract AI/ML concepts from medium vacancy 14."
            },
            {
                "question": "====TEXT of VACANCY====\nDevOps Engineer. Required: Docker, Kubernetes, Terraform, Ansible. Nice-to-have: Jenkins, GitHub Actions. No experience with ArgoCD needed.\n====END TEXT====\n\nExtract: Title, Docker, Kubernetes, Terraform, Ansible, Jenkins, GitHub_Actions, ArgoCD. Example: {\"Title\": \"Role\", \"Docker\": \"no\", \"Kubernetes\": \"no\", \"Terraform\": \"no\", \"Ansible\": \"no\", \"Jenkins\": \"no\", \"GitHub_Actions\": \"no\", \"ArgoCD\": \"no\"}",
                "expected_json": {"Title": "DevOps Engineer", "Docker": "required", "Kubernetes": "required",
                                  "Terraform": "required", "Ansible": "required", "Jenkins": "nice-to-have",
                                  "GitHub_Actions": "nice-to-have", "ArgoCD": "no"},
                "summary": "Extract DevOps tools from medium vacancy 15."
            },
            {
                "question": "====TEXT of VACANCY====\nWe are hiring a Senior Software Engineer. The role is fully remote, based in the USA. Salary is 120k-150k USD per year. We offer health insurance, 401k, and 20 days PTO. You need 5+ years of experience and a Bachelor's degree. The tech stack includes Python, SQL, and AWS.\n====END TEXT====\n\nExtract: Title, EmploymentType, CandidateCountry, SalaryMin, SalaryMax, SalaryCurrency, SalaryPeriod, HealthInsurance, RetirementPlan, PaidTimeOffDays, MinYearsExperience, EducationLevel, Python, SQL, AWS. Example: {\"Title\": \"Role\", \"EmploymentType\": \"office\", \"CandidateCountry\": [\"UK\"], \"SalaryMin\": \"50000\", \"SalaryMax\": \"75000\", \"SalaryCurrency\": \"EUR\", \"SalaryPeriod\": \"year\", \"HealthInsurance\": \"no\", \"RetirementPlan\": \"no\", \"PaidTimeOffDays\": 10, \"MinYearsExperience\": 2, \"EducationLevel\": \"high-school\", \"Python\": \"no\", \"SQL\": \"no\", \"AWS\": \"no\"}",
                "expected_json": {"Title": "Senior Software Engineer", "EmploymentType": "remote",
                                  "CandidateCountry": ["USA"], "SalaryMin": "120000", "SalaryMax": "150000",
                                  "SalaryCurrency": "USD", "SalaryPeriod": "year", "HealthInsurance": "yes",
                                  "RetirementPlan": "yes", "PaidTimeOffDays": 20, "MinYearsExperience": 5,
                                  "EducationLevel": "bachelor", "Python": "required", "SQL": "required",
                                  "AWS": "required"},
                "summary": "Extract comprehensive details from long vacancy 16."
            },
            {
                "question": "====TEXT of VACANCY====\nContract Data Analyst needed for a 6-month project. Probation is 1 month, notice period is 2 weeks. Working 40 hours/week. The company is a scale-up in the Financial Services industry. Team size is 10, reporting to the Head of Data. We are hiring 1 person. Minimum 3 years experience, Bachelor's degree required. Tech: SQL, Python, Tableau.\n====END TEXT====\n\nExtract: Title, ContractType, ContractDurationMonths, ProbationPeriodMonths, NoticePeriodWeeks, WorkingHoursPerWeek, CompanyStage, CompanyIndustry, TeamSize, ReportingTo, NumberOfOpenPositions, MinYearsExperience, EducationLevel, SQL, Python, Tableau. Example: {\"Title\": \"Role\", \"ContractType\": \"permanent\", \"ContractDurationMonths\": 12, \"ProbationPeriodMonths\": 3, \"NoticePeriodWeeks\": 4, \"WorkingHoursPerWeek\": 37.5, \"CompanyStage\": \"startup\", \"CompanyIndustry\": \"Tech\", \"TeamSize\": 5, \"ReportingTo\": \"Manager\", \"NumberOfOpenPositions\": 2, \"MinYearsExperience\": 1, \"EducationLevel\": \"master\", \"SQL\": \"no\", \"Python\": \"no\", \"Tableau\": \"no\"}",
                "expected_json": {"Title": "Contract Data Analyst", "ContractType": "contract",
                                  "ContractDurationMonths": 6, "ProbationPeriodMonths": 1, "NoticePeriodWeeks": 2,
                                  "WorkingHoursPerWeek": 40, "CompanyStage": "scale-up",
                                  "CompanyIndustry": "Financial Services", "TeamSize": 10,
                                  "ReportingTo": "Head of Data", "NumberOfOpenPositions": 1, "MinYearsExperience": 3,
                                  "EducationLevel": "bachelor", "SQL": "required", "Python": "required",
                                  "Tableau": "required"},
                "summary": "Extract contract, company, experience, tech from long vacancy 17."
            },
            {
                "question": "====TEXT of VACANCY====\nBackend Developer role. Required languages: English. Background check required, no drug screening, NDA required, no non-compete. Job ID: 987654. Posted on Indeed. Apply at https://apply.co. Posted 2 days ago, 50 applicants. Tech: Java, Spring Boot, PostgreSQL.\n====END TEXT====\n\nExtract: Title, RequiredLanguages, BackgroundCheck, DrugScreening, NDARequired, NonCompeteRequired, JobId, VacancySite, ApplyURL, PublicationDate, ApplicantsCount, Java, Spring_Boot, PostgreSQL. Example: {\"Title\": \"Role\", \"RequiredLanguages\": [\"German\"], \"BackgroundCheck\": \"no\", \"DrugScreening\": \"yes\", \"NDARequired\": \"no\", \"NonCompeteRequired\": \"yes\", \"JobId\": \"000\", \"VacancySite\": \"LinkedIn\", \"ApplyURL\": \"url\", \"PublicationDate\": \"1 day ago\", \"ApplicantsCount\": \"10\", \"Java\": \"no\", \"Spring_Boot\": \"no\", \"PostgreSQL\": \"no\"}",
                "expected_json": {"Title": "Backend Developer", "RequiredLanguages": ["English"],
                                  "BackgroundCheck": "yes", "DrugScreening": "no", "NDARequired": "yes",
                                  "NonCompeteRequired": "no", "JobId": "987654", "VacancySite": "Indeed",
                                  "ApplyURL": "https://apply.co", "PublicationDate": "2 days ago",
                                  "ApplicantsCount": "50", "Java": "required", "Spring_Boot": "required",
                                  "PostgreSQL": "required"},
                "summary": "Extract conditions, metadata, tech from long vacancy 18."
            },
            {
                "question": "====TEXT of VACANCY====\nAI Research Scientist. You will work with Deep Learning, Neural Networks, NLP, and LLMs. Experience with PyTorch, TensorFlow, and RAG is required. Nice-to-have: Prompt Engineering, Fine-Tuning. Soft skills: Communication, Teamwork, Problem Solving, Critical Thinking.\n====END TEXT====\n\nExtract: Title, Deep_Learning, Neural_Networks, NLP, LLMs, PyTorch, TensorFlow, RAG, Prompt_Engineering, Fine_Tuning, Communication, Teamwork, Problem_Solving, Critical_Thinking. Example: {\"Title\": \"Role\", \"Deep_Learning\": \"no\", \"Neural_Networks\": \"no\", \"NLP\": \"no\", \"LLMs\": \"no\", \"PyTorch\": \"no\", \"TensorFlow\": \"no\", \"RAG\": \"no\", \"Prompt_Engineering\": \"no\", \"Fine_Tuning\": \"no\", \"Communication\": \"no\", \"Teamwork\": \"no\", \"Problem_Solving\": \"no\", \"Critical_Thinking\": \"no\"}",
                "expected_json": {"Title": "AI Research Scientist", "Deep_Learning": "required",
                                  "Neural_Networks": "required", "NLP": "required", "LLMs": "required",
                                  "PyTorch": "required", "TensorFlow": "required", "RAG": "required",
                                  "Prompt_Engineering": "nice-to-have", "Fine_Tuning": "nice-to-have",
                                  "Communication": "required", "Teamwork": "required", "Problem_Solving": "required",
                                  "Critical_Thinking": "required"},
                "summary": "Extract AI/ML and soft skills from long vacancy 19."
            },
            {
                "question": "====TEXT of VACANCY====\nFull Stack Data Warehouse Developer. Remote, USA. Salary 100k-130k USD/year. Health insurance, 401k, 25 days PTO, 5000 learning budget. 5+ years experience, Bachelor's degree. Tech: Python, SQL, dbt, Apache Airflow, Star Schema, Snowflake Schema. 3 interview rounds, technical assessment, no coding challenge. Urgency: within-1-month.\n====END TEXT====\n\nExtract: Title, EmploymentType, CandidateCountry, SalaryMin, SalaryMax, SalaryCurrency, SalaryPeriod, HealthInsurance, RetirementPlan, PaidTimeOffDays, LearningBudget, MinYearsExperience, EducationLevel, Python, SQL, dbt, Apache_Airflow, Star_Schema, Snowflake_Schema, InterviewRounds, TechnicalAssessment, CodingChallenge, Urgency. Example: {\"Title\": \"Role\", \"EmploymentType\": \"office\", \"CandidateCountry\": [\"UK\"], \"SalaryMin\": \"50000\", \"SalaryMax\": \"75000\", \"SalaryCurrency\": \"EUR\", \"SalaryPeriod\": \"year\", \"HealthInsurance\": \"no\", \"RetirementPlan\": \"no\", \"PaidTimeOffDays\": 10, \"LearningBudget\": \"1000\", \"MinYearsExperience\": 2, \"EducationLevel\": \"master\", \"Python\": \"no\", \"SQL\": \"no\", \"dbt\": \"no\", \"Apache_Airflow\": \"no\", \"Star_Schema\": \"no\", \"Snowflake_Schema\": \"no\", \"InterviewRounds\": 2, \"TechnicalAssessment\": \"no\", \"CodingChallenge\": \"yes\", \"Urgency\": \"immediate\"}",
                "expected_json": {"Title": "Full Stack Data Warehouse Developer", "EmploymentType": "remote",
                                  "CandidateCountry": ["USA"], "SalaryMin": "100000", "SalaryMax": "130000",
                                  "SalaryCurrency": "USD", "SalaryPeriod": "year", "HealthInsurance": "yes",
                                  "RetirementPlan": "yes", "PaidTimeOffDays": 25, "LearningBudget": "5000",
                                  "MinYearsExperience": 5, "EducationLevel": "bachelor", "Python": "required",
                                  "SQL": "required", "dbt": "required", "Apache_Airflow": "required",
                                  "Star_Schema": "required", "Snowflake_Schema": "required", "InterviewRounds": 3,
                                  "TechnicalAssessment": "yes", "CodingChallenge": "no", "Urgency": "within-1-month"},
                "summary": "Extract full details from long vacancy 20."
            }
        ]

        # Generating remaining 30 questions programmatically to ensure variety and length increase
        # while keeping the file size manageable and strictly following the format.
        subjects = [
            ("Frontend Developer", "React, TypeScript, CSS, HTML, Webpack, Vite",
             "Communication, Teamwork, Adaptability", "Health insurance, 20 days PTO", "3 rounds, technical test",
             "Bachelor's, 3 years", "remote", "USA", "80000", "110000", "USD", "year"),
            ("Data Engineer", "Python, SQL, Spark, Kafka, AWS, dbt", "Problem Solving, Critical Thinking",
             "401k, learning budget 2000", "4 rounds, no coding challenge", "Master's, 5 years", "hybrid", "UK",
             "90000", "120000", "GBP", "year"),
            ("DevOps Engineer", "Docker, Kubernetes, Terraform, Ansible, Jenkins", "Leadership, Time Management",
             "Stock options, unlimited PTO", "2 rounds, system design", "Bachelor's, 4 years", "remote", "Canada",
             "100000", "140000", "CAD", "year"),
            ("Product Manager", "Jira, Confluence, Figma, SQL", "Negotiation, Empathy, Decision Making",
             "Health, dental, 15 days PTO", "3 rounds, case study", "Bachelor's, 6 years", "office", "Germany", "70000",
             "95000", "EUR", "year"),
            ("QA Automation Engineer", "Python, Selenium, PyTest, Jenkins, Docker", "Attention to Detail, Patience",
             "Gym membership, 22 days PTO", "3 rounds, coding challenge", "Bachelor's, 3 years", "remote", "Australia",
             "85000", "105000", "AUD", "year"),
            ("Machine Learning Engineer", "Python, PyTorch, TensorFlow, NLP, LLMs", "Creativity, Analytical Thinking",
             "Health, 401k, 25 days PTO", "4 rounds, technical assessment", "PhD, 2 years", "hybrid", "France", "60000",
             "85000", "EUR", "year"),
            ("Backend Developer", "Java, Spring Boot, PostgreSQL, Redis, Kafka", "Collaboration, Work Ethic",
             "Meal allowance, 20 days PTO", "3 rounds, take-home assignment", "Bachelor's, 4 years", "remote",
             "Netherlands", "75000", "95000", "EUR", "year"),
            ("UI/UX Designer", "Figma, Sketch, Adobe XD, User Research", "Empathy, Communication, Creativity",
             "Health, 18 days PTO, learning budget", "3 rounds, portfolio review", "Bachelor's, 3 years", "hybrid",
             "Spain", "50000", "70000", "EUR", "year"),
            ("Cloud Architect", "AWS, Azure, GCP, Terraform, Kubernetes", "Strategic Thinking, Leadership",
             "Stock options, 30 days PTO", "4 rounds, architecture review", "Master's, 8 years", "remote", "USA",
             "150000", "200000", "USD", "year"),
            ("Security Engineer", "Python, Bash, Linux, Wireshark, Splunk", "Critical Thinking, Attention to Detail",
             "Health, 401k, 25 days PTO", "3 rounds, technical test", "Bachelor's, 5 years", "office", "UK", "90000",
             "120000", "GBP", "year"),
            ("Mobile Developer", "Swift, Kotlin, React Native, Firebase", "Adaptability, Problem Solving",
             "Health, 20 days PTO, gym", "3 rounds, coding challenge", "Bachelor's, 3 years", "remote", "Canada",
             "80000", "110000", "CAD", "year"),
            ("Site Reliability Engineer", "Go, Python, Kubernetes, Prometheus, Grafana", "Stress Management, Teamwork",
             "Unlimited PTO, stock options", "3 rounds, system design", "Bachelor's, 4 years", "hybrid", "Germany",
             "85000", "115000", "EUR", "year"),
            ("Business Analyst", "SQL, Excel, Tableau, Power BI", "Communication, Analytical Thinking",
             "Health, 22 days PTO", "2 rounds, case study", "Bachelor's, 2 years", "office", "Australia", "70000",
             "90000", "AUD", "year"),
            ("Network Engineer", "Cisco, Juniper, Python, BGP, OSPF", "Problem Solving, Attention to Detail",
             "Health, 20 days PTO", "3 rounds, technical test", "Bachelor's, 5 years", "remote", "France", "65000",
             "85000", "EUR", "year"),
            ("Scrum Master", "Jira, Confluence, Agile, Scrum", "Leadership, Empathy, Communication",
             "Health, 25 days PTO, learning budget", "2 rounds, behavioral", "Bachelor's, 4 years", "hybrid",
             "Netherlands", "70000", "90000", "EUR", "year"),
            ("Database Administrator", "PostgreSQL, MySQL, Oracle, SQL Server", "Attention to Detail, Problem Solving",
             "Health, 401k, 20 days PTO", "3 rounds, technical assessment", "Bachelor's, 5 years", "office", "Spain",
             "60000", "80000", "EUR", "year"),
            ("Technical Writer", "Markdown, Git, Confluence, Jira", "Written Communication, Attention to Detail",
             "Health, 20 days PTO, remote work", "2 rounds, writing test", "Bachelor's, 2 years", "remote", "USA",
             "70000", "90000", "USD", "year"),
            ("Game Developer", "C++, Unreal Engine, Unity, C#", "Creativity, Teamwork, Problem Solving",
             "Health, 20 days PTO, game allowance", "3 rounds, coding challenge", "Bachelor's, 3 years", "office", "UK",
             "60000", "85000", "GBP", "year"),
            ("Systems Administrator", "Linux, Windows, Bash, PowerShell, Ansible", "Problem Solving, Time Management",
             "Health, 22 days PTO", "3 rounds, technical test", "Bachelor's, 4 years", "hybrid", "Canada", "75000",
             "95000", "CAD", "year"),
            ("Data Scientist", "Python, R, SQL, Machine Learning, Pandas", "Analytical Thinking, Communication",
             "Health, 401k, 25 days PTO", "4 rounds, technical assessment", "Master's, 3 years", "remote", "Germany",
             "80000", "110000", "EUR", "year"),
            ("Frontend Architect", "React, TypeScript, Node.js, GraphQL, AWS", "Leadership, Strategic Thinking",
             "Stock options, 30 days PTO", "4 rounds, architecture review", "Master's, 8 years", "remote", "USA",
             "160000", "210000", "USD", "year"),
            ("Embedded Systems Engineer", "C, C++, RTOS, ARM, Linux", "Attention to Detail, Problem Solving",
             "Health, 20 days PTO", "3 rounds, technical test", "Bachelor's, 5 years", "office", "UK", "70000", "95000",
             "GBP", "year"),
            ("IT Support Specialist", "Windows, macOS, Active Directory, Office 365", "Customer Service, Patience",
             "Health, 15 days PTO", "2 rounds, practical test", "High-school, 1 year", "office", "Australia", "50000",
             "65000", "AUD", "year"),
            ("Blockchain Developer", "Solidity, Rust, Ethereum, Web3, Smart Contracts",
             "Analytical Thinking, Problem Solving", "Crypto bonuses, 25 days PTO", "3 rounds, coding challenge",
             "Bachelor's, 3 years", "remote", "Switzerland", "100000", "150000", "CHF", "year"),
            ("Growth Hacker", "SQL, Python, Google Analytics, A/B Testing", "Creativity, Analytical Thinking",
             "Health, 20 days PTO, performance bonus", "3 rounds, case study", "Bachelor's, 3 years", "hybrid",
             "Netherlands", "65000", "85000", "EUR", "year"),
            ("Solutions Architect", "AWS, Azure, GCP, Terraform, Microservices", "Strategic Thinking, Communication",
             "Stock options, 30 days PTO", "4 rounds, architecture review", "Master's, 7 years", "remote", "USA",
             "140000", "190000", "USD", "year"),
            ("Quality Assurance Lead", "Python, Selenium, Cypress, Jenkins, Jira", "Leadership, Attention to Detail",
             "Health, 401k, 25 days PTO", "3 rounds, technical assessment", "Bachelor's, 6 years", "hybrid", "UK",
             "80000", "110000", "GBP", "year"),
            ("Full Stack Engineer", "JavaScript, TypeScript, React, Node.js, PostgreSQL", "Teamwork, Problem Solving",
             "Health, 20 days PTO, learning budget", "3 rounds, coding challenge", "Bachelor's, 4 years", "remote",
             "Canada", "90000", "120000", "CAD", "year"),
            ("Machine Learning Ops Engineer", "Python, Docker, Kubernetes, MLflow, AWS", "Problem Solving, Automation",
             "Health, 401k, 25 days PTO", "3 rounds, technical test", "Bachelor's, 4 years", "remote", "Germany",
             "85000", "115000", "EUR", "year"),
            ("Chief Technology Officer", "Strategic Planning, Team Leadership, Architecture",
             "Leadership, Strategic Thinking, Vision", "Equity, 40 days PTO, executive benefits",
             "3 rounds, executive interview", "Master's, 15 years", "hybrid", "USA", "200000", "300000", "USD", "year")
        ]

        for idx, (title, tech, soft_skills, benefits, process, edu_exp, location_type, country, sal_min, sal_max,
                  currency, period) in enumerate(subjects):
            tech_list = [t.strip() for t in tech.split(",")]
            tech_keys = [t.replace(" ", "_").replace("-", "_") for t in tech_list]
            soft_list = [s.strip() for s in soft_skills.split(",")]
            soft_keys = [s.replace(" ", "_").replace("-", "_") for s in soft_list]

            text = f"We are hiring a {title}. Location: {location_type}, {country}. Salary: {sal_min}-{sal_max} {currency} per {period}. "
            text += f"Benefits include: {benefits}. "
            text += f"Hiring process: {process}. "
            text += f"Requirements: {edu_exp}. "
            text += f"Tech stack: {tech}. "
            text += f"Soft skills: {soft_skills}."

            keys = ["Title", "EmploymentType", "CandidateCountry", "SalaryMin", "SalaryMax", "SalaryCurrency",
                    "SalaryPeriod"]
            keys.extend(tech_keys)
            keys.extend(soft_keys)

            expected = {
                "Title": title,
                "EmploymentType": location_type,
                "CandidateCountry": [country],
                "SalaryMin": sal_min,
                "SalaryMax": sal_max,
                "SalaryCurrency": currency,
                "SalaryPeriod": period
            }
            for t, tk in zip(tech_list, tech_keys):
                expected[tk] = "required"
            for s, sk in zip(soft_list, soft_keys):
                expected[sk] = "required"

            example = {
                "Title": "Example Role",
                "EmploymentType": "remote",
                "CandidateCountry": ["USA"],
                "SalaryMin": "50000",
                "SalaryMax": "75000",
                "SalaryCurrency": "USD",
                "SalaryPeriod": "year"
            }
            for tk in tech_keys:
                example[tk] = "required"
            for sk in soft_keys:
                example[sk] = "required"

            keys_str = ", ".join([f'"{k}"' for k in keys])
            prompt = f"====TEXT of VACANCY====\n{text}\n====END TEXT====\n\nExtract the following details and return ONLY a valid JSON object with these exact keys: {keys_str}. Do not add any markdown formatting, extra text, or explanations. Example JSON format: {json.dumps(example)}"

            questions.append({
                "question": prompt,
                "expected_json": expected,
                "summary": f"Extract details from vacancy {21 + idx}."
            })

        return questions