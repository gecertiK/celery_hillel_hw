# celery_hillel_hw

Steps to create a new project in terminal
1) cd PycharmProjects
2) mkdir <name of projects>
3) cd <name of projects>
4) python3 -m venv .venv - create virtual
5) source .venv/bin/activate
6) pip install -U pip
7) pip install django
8) django-admin startproject <name> .
9) open project in PyCharm
10) ALWAYS HIDE SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")!!!!!!!!!!!!!!!!!!!
11) add .gitignore/README.md
12) install flake8/travis ang configure
13) pip freeze > requirements.txt
14) create a new branch
