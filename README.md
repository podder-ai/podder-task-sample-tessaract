# podder-task

This is base repository for PoC (Proof of Concept) code.
Boilerplate project for creating python task using the [podder-pipeline](https://github.com/podder-ai/podder-pipeline).

## How to implement your code

### Source code directory

```
$ tree . -L 2
.
├── Dockerfile
├── README.md
├── api
│   ├── __init__.py
│   ├── grpc_server.py
│   ├── protos
│   └── task_api.py
├── app
│   ├── __init__.py
│   └── task.py             # main task implementation
├── log.yml
├── main.py
├── requirements
│   ├── requirements.develop.txt
│   └── requirements.txt    # add required packages here
├── run_codegen.py
├── scripts
│   ├── entrypoint.sh
│   └── pre-commit.sh       # execute before committing your codes
├── shared
│   ├── data
│   └── tmp
└── tests
    ├── files
    │   └── inputs.json     # sample inputs.json
    └── unit                # add unit test here
```

### How to implement a task class

Add your code to `app/task.py`.

#### Implementation sample

Please check task sample here [Sample](https://github.com/podder-ai/podder-task-sample)

#### __init__: Initialize task instance

```python
def __init__(self, context: Context) -> None:
    self.logger.debug("Initiate task...")
    super().__init__(context)
```

#### execute: Main process

```python
def execute(self) -> None:

    self.logger.debug("START processing...")

    self.yourProcess(self.args.input_path)

    self.logger.debug("Completed.")

```

#### set_arguments: Arguments

```python
def set_arguments(self, parser) -> None:

    parser.add_argument('--input_path', dest="input_path", help='set input path', default='.')

```

### API

`podder-task-base` python module provides many APIs for the development.

#### Logging

You can output logs with `self.logger`. `logger` is just a wrapper of logging. For further logging usage, please check [here](https://docs.python.org/3.6/library/logging.html)

```python
self.logger.debug("debug")
self.logger.info("info")
```

#### Command Line Arguments

You can add your own command line argument using `self.context.config.set_argument` within `task.py`.

After you execute with command line arguments, you can access to the passed arguments through `self.context.config.get`.

For example, set `--model` to command line argument.

```python
# Set your command line argument
def set_arguments(self) -> None:
    self.context.config.set_argument('--model-path', dest="model_path", help='set model path')
```

```bash
# Execute main.py with argument "--model"
$ python main.py --model-path /path/to/model
```

```python
# You can access to the value passed to "--model"
def execute(self, inputs: List[Any]) -> List[Any]:
    model = self.context.config.get('model_path')
```

#### Shared directories

There are 4 shared directories, which is `config`, `input`, `output`, `tmp`. 
They are shared among the environment and every containers can access them.

- `config`: Where config files are located.
- `input`:  Where input files are located.
- `output`: Where output files are located.
- `tmp`:    Where temporary files are located. Podder Pipeline creates the 
  directory under the `tmp/dag_id/job_id` to keep each job's temporary files.

When you need to locate the temporary files, please put them into `tmp` directory.
You can get the path to `tmp` directory by `self.context.file.get_tmp_path(file_name)`. 

```python
self.context.file.get_tmp_path('sample.csv')
# => /path/to/shared/tmp/sample.csv
```

## How to run Podder Task

### Run on Docker

We strongly recommend to run Podder Task using Docker.

- Build docker image

```bash
$ docker build -t podder-task .
```

- Execute on the docker container

```bash
$ docker run -it --env-file .env.example podder-task bash

# You can run your code
$ python main.py --inputs tests/files/inputs.json
```

- Run with one-liner

If you want to run it with one-liner code, you can also run it.

```bash
$ docker run -it --env-file .env.example podder-task python main.py --inputs tests/files/inputs.json
```

### Run on local

#### For Mac os, Linux user

```bash
# clone podder-task
$ git clone git@github.com:podder-ai/podder-task.git
$ cd podder-task
# enable python3
$ python3 -m venv env
$ source env/bin/activate
# install required libraries
$ pip install -r requirements.txt
# run sample code
$ python main.py --inputs /path/to/input/a /path/to/input/b
```

#### For Windows user with PowerShell

If using Powershell, the activate script is subject to the execution policies on the system. By default on Windows 7, the system's excution policy is set to `Restricted`, meaning no scripts as virtualenv activation script are allowed to be executed.

In order to use the script, you can relax your system's execution policy to `Unrestricted`, meaning all scripts on the system can be executed. As an administrator run:

```
C:\>Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force -Verbose
```

```bash
# clone podder-task
C:\> git clone git@github.com:podder-ai/podder-task.git
C:\> cd podder-task
# enable python3
C:\>python3 -m venv C:\path\to\myenv
# Windows cmd.exe
C:\> C:\path\to\myenv\Scripts\activate.bat
# PowerShell PS
C:\> C:\path\to\myenv\Scripts\Activate.ps1
# install required libraries
C:\> pip install -r requirements.txt
# run sample code
C:\> python main.py --inputs /path/to/input/a /path/to/input/b
```

## Configuration

Copy and create `.env` file and add your env variables.

```bash
$ cp .env.sample .env
```

## Linter, Formatter and Unit Test

Please execute linters, formatters and unit tests before committing your source codes.

### How To Execute

You can execute them by the following command.
Make sure that you are under the root directory of your project. (e.q. podder-task/)
```
$ pip install -r ./requirements/requirements.develop.txt
$ sh ./scripts/pre-commit.sh
```

### Supported Libraries

#### Linter

- flake8

#### Formatter

- autopep8
- yapf
- autoflake
- isort

#### Unit Test

- pytest

### Rules of Development
Please follow the official documents of the libraries.

### How To Execute Unit Test
```
$ cd podder-task
$ docker build . -t podder-task
$ docker run --env-file .env.example -t podder-task pytest
```

## Implementation note

Finally, your task implementation will be integrated to Podder-Pipeline and deploy using Docker/Kubernetes.
To make it easier, please follow this implementation rules below.

- Only add your code to `app/task.py`
- Put your data set or model files to `data`
- Your task implementation will be compiled by Cython in integrating. Please don't use `__file__` in your code.
- Create virtual environment for your code. Please check [Creation of virtual environments](https://docs.python.org/3/library/venv.html)

Please add issue & pull request if you have any request!
