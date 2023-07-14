# Github Repository Clone

## Author

**Name**: Ismaël Maurice

**Github**: https://github.com/tisma95

**Email**: ismael.tuo@edigrp.com <br>

## Description

This repository goal is to clone all repositories of github associate to the user.

If the repository existed pull the updated code.

Clone all branchs in folder.

## Requirement

Before starting the project you need to install on your computer the following packages:

[Python >=3.9](https://www.python.org/downloads/)

[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)


## Started

Run the commands inside the folder:

1. If no **env** folder exists init the environment else skip this step
```cmd
    python -m venv env
```
or
```cmd
    python3 -m venv env
```
or for ubuntu
```cmd
    virtualenv venv
```

```node
    If any problem follow this page to fix and intall virutalenv: https://gist.github.com/frfahim/73c0fad6350332cef7a653bcd762f08d
```

2. If the env folder already exists, run the following command to activate it
```cmd
    source env/bin/activate
```

3 Run the installation of package via following command
```cmd
    pip install -r requirements.txt
```

4. Init the environment variable by following [Environment variables](#environment-variables)

5. Run the script with command `python main.py` or `python3 main.py`

## Environment variables ##

Create the file **.env** inside folder with following example variable

```yaml
# Clone repo host
DOMAIN = github.com
# Access Token To Domain
TOKEN = toto
# Storage Folder => Folder where the repositories will be save
FOLDER = repos
```

## Other informations

+ If new package is install we can update the **requirements.txt** with command `pip freeze > requirements.txt` or `python3 -m pip freeze > requirements.txt`

+ Exit the env via: `deactivate`


## Useful packages

[Requests Documentation](https://requests.readthedocs.io/en/latest/user/quickstart/)

[Github REST API Documentation](https://docs.github.com/en/rest?apiVersion=2022-11-28)

[python-dotenv Documentation](https://pypi.org/project/python-dotenv/)
