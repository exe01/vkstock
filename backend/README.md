How to install djnatimat
========================

```bash
pip install git+git://github.com/arsensokolov/djantimat.git#egg=djantimat
python manage.py migrate
python manage.py loaddata --app djantimat initial_data # для добавления существующей базы слов
```