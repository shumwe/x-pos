@echo off

@REM Create Virtual Environment within the folder
py -m venv env

@REM Activate Virtual Environment
env\Scripts\activate

@REM Install requirements In Virtual Environment
pip install -r requirements.txt

@Rem Run App Migrations
python manage.py makemigrations
python manage.py migrate