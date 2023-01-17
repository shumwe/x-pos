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
