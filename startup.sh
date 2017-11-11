virtualenv .ve -p python3 && source .ve/bin/activate && pip install -r requirements.txt && ./manage.py migrate && ./manage.py runserver

