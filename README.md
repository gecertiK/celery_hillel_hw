# celery_hillel_hw

Steps to create a new project in terminal

cd PycharmProjects
mkdir
cd
python3 -m venv .venv - create virtual
source .venv/bin/activate
pip install -U pip
pip install django
django-admin startproject <name> .
open project in PyCharm
ALWAYS HIDE SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")!!!!!!!!!!!!!!!!!!!
add .gitignore/README.md
install flake8/travis ang configure
pip freeze > requirements.txt
create a new branch
