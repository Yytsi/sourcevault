# sourcevault

![Workflow badge](https://github.com/Yytsi/sourcevault/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/Yytsi/sourcevault/graph/badge.svg?token=2QSRCPDGGL)](https://codecov.io/gh/Yytsi/sourcevault)  

[Github Actions](https://github.com/Yytsi/sourcevault/actions)

[Backlog](https://docs.google.com/spreadsheets/d/1Kn8T_J5zpqmHX5HLiwrYFkmAaxSycxQrstnDQTh-bX0/edit#gid=427790378)

## Installation

1. Clone this repository or [download the newest release](https://github.com/Yytsi/sourcevault/releases)  

2. Navigate to the project's root folder   

3. Install dependencies with  
```
poetry install
```

4. Create .env file with the following contents
```
AWS_ACCESS_KEY_ID= <key id>
AWS_SECRET_ACCESS_KEY= <secret access key>
AWS_BUCKET_NAME= <aws bucket name>
```

5. Enter virtual environment with
```
poetry shell
```

6. Run application with  
```
python src/index.py
```
