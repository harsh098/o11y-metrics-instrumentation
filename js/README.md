# Setup the Repo
```
git clone  git@github.com:harsh098/o11y-metrics-instrumentation.git
cd o11y-metrics-instrumentation/js
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

# Setup JavaScript Express App
In the same directory
```
npm i
export OTEL_SERVICE_NAME=express  #Replace with the name of your choice.
npm run server  #This will start an express server at 8000
```