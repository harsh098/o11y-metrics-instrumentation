# Zero Code Instrumentations
This repo contains boilerplate code for Zero Code instrumentation with or without OpenTelemetry

# Directory structure

```
├── README.md
├── alloy  # Alloy Configurations and Docker Compose
├── dashboards # Grafana Dashboards
├── django # Django Instrumentations
├── docker-compose.yaml # Global Docker Compose for Grafana
├── fast-api-instrumentation-v2 # Fast API Instrumentation with FastAPI (This version emulates all possible HTTP Methods)
├── fast-api-instrumentor # Fast API Instrumentation with FastAPI (This version only includes a healthcheck)
├── flaskapi-instrumentation # Flask API Instrumentation
├── js # Express App without OpenTelemetry (uses Prometheus Middleware to Expose Metrics)
├── loki # Loki Configuration and Docker Compose [WIP: Will Update when I'll work on logging] 
├── prometheus # Prometheus Configuration and Docker Compose
└── tempo # Tempo Configuration and Docker Compose
```  

Head on to individual directories for detailed instructions on how to run each app.

