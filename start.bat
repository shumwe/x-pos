@echo off
rem Activate the virtual environment
call .env\bin\Scripts\activate.bat

rem Run the Django development server
start python manage.py runserver & start http://127.0.0.1:8000/

rem Open the app in a browser