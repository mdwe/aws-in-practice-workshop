# AWS in practise - Workshop

# 1. Usage of AWS services in serverless architecture

## Requirements 
- AWS account with free tier
- Basic knowledge about Python and API
- Postman installed
- Python 3.7 installed

## Exercises
1. [Create RESTful API based on AWS services](instructions/1_services_in_serverless_architecture/ex1/ex1.md)
2. [Create solution for 3rd part systems to modify products state](instructions/1_services_in_serverless_architecture/ex2/ex2.md)

## How to start

1. Install project requirements:

    ```
    pip install -r requirements.txt
    ```

2. Install pre-commit hooks

    ```
    pre-commit install
    ```

    You can run pre-commmit manually: 

    ```
    pre-commit run --all-files
    ```

## Tests

Test framework: `unittest`

Additional tools for tests: `boto3`, `moto`

Execution tests with console command (in project root):

```
python -m unittest discover -v lambdas/tests
```


## Additional information

### Common tools 

1. `Pre-commit` - A framework for managing and maintaining multi-language pre-commit hooks. [Read more](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Python libraries

1. `Boto3` - Boto is the Amazon Web Services (AWS) SDK for Python. It enables Python developers to create, configure, and manage AWS services, such as EC2 and S3. Boto provides an easy to use, object-oriented API, as well as low-level access to AWS services. [Read more](http://docs.getmoto.org/en/latest/)
2. `Moto` - A library that allows you to easily mock out tests based on AWS infrastructure. [Read more](http://docs.getmoto.org/en/latest/)


### Python tools

1. `Flake8` - is a Python library that wraps PyFlakes, pycodestyle and Ned Batchelder's McCabe script. It is a great toolkit for checking your code base against coding style (PEP8), programming errors (like “library imported but unused" and “Undefined name") and to check cyclomatic complexity. [Read more](https://simpleisbetterthancomplex.com/packages/2016/08/05/flake8.html)

2. `Black` - is a Python code formatter. By using it, you agree to cede control over minutiae of hand-formatting. In return, Black gives you speed, determinism, and freedom from pycodestyle nagging about formatting. You will save time and mental energy for more important matters.
Blackened code looks the same regardless of the project you're reading. Formatting becomes transparent after a while and you can focus on the content instead.
Black makes code review faster by producing the smallest diffs possible. [Read more](https://pypi.org/project/black/)


# 2. Automatization and management of infrastructure and services