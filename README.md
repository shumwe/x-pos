# Point Of Sell

## Running

clone the website from github

``` bash
git clone https://github.com/shumwe/x-pos.git
cd x-pos
```

Create a virtual environment

``` bash
python -m venv .env
source .env/in/activate

```

Install the requirements

``` bash
pip install --upgrade pip
pip install -r requirements.txt
```

Make and run migrations

``` bash
python manage.py makemigrations
python manage.py migrate
```

Run the application

``` bash
pythton manage.py runserver
```

## Installing

ensure python is installed

``` bash
python --version
```

build the project

``` text
double click build.bat
```

run the project

``` text
double click run.bat
```

```

password: Pos12345
username: admin

```