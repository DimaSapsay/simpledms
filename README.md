simpledms
-----------------

Simple DMS (document management system)

## Підготувати середовище
```bash
virtualenv -p python3 venv
source ./venv/bin/activate
```
## Встановити залежності
```bash
pip install -r requirements.txt
```
## Запустити worker
```bash
celery -A simpledms worker -l INFO
```
## Запустити проект
```bash
python manage.py runserver
```
## Посилання на swagger
http://127.0.0.1:8000/swagger/
