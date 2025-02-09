
# Setup the Repo
```
git clone  git@github.com:harsh098/o11y-metrics-instrumentation.git
cd o11y-metrics-instrumentation/django
```

# Setup Load Emulation with Locust
## Setup Locust
In the same directory
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Load Emulation with Locust
In the same Directory.
```
source venv/bin/activate
locust -f locustfile.py
```  
This will open a browser window at http://0.0.0.0:8089/

# Start the Django Server
In the same directory
```
source venv/bin/activate
cd django_instrumentor
python manage.py makemigrations && python manage.py migrate
python manage.py runserver
```