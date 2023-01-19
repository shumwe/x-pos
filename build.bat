@echo off

@REM Remove any environments
rm -rf .env/
rm -rf c:\.env

@REM create virtual environment
python -m venv c:\.env

rem Activate the virtual environment
@REM call %cd%\.env\bin\Scripts\activate.bat
call c:\.env

pip install -r requirements.txt

rem run migrations
python manage.py makemigrations
python manage.py migrate