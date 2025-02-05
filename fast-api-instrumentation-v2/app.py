from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import Optional
from opentelemetry import trace, metrics
#from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import asyncio
import random

METRICS_FILE=open("./metrics_data.txt", mode="w", encoding="utf-8")
# Initialize OpenTelemetry
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Set up OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint="127.0.0.1:4417", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
otlp_metric_exporter = OTLPMetricExporter(endpoint="http://127.0.0.1:9090/api/v1/otlp/v1/metrics")
console_exporter = ConsoleMetricExporter(out=METRICS_FILE)
console_reader = PeriodicExportingMetricReader(console_exporter)
reader = PeriodicExportingMetricReader(otlp_metric_exporter, export_interval_millis=5000)

trace.get_tracer_provider().add_span_processor(span_processor)
meter_provider = MeterProvider(metric_readers=[reader, console_reader])
metrics.set_meter_provider(meter_provider)

app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "name": f"Item {item_id}"}

@app.post("/items/")
async def create_item(item: Item):
    if item.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
    return {"message": "Item created", "item": item}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be positive")
    return {"message": "Item updated", "item_id": item_id, "item": item}

@app.patch("/items/{item_id}")
async def partial_update_item(item_id: int, item: Item):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item partially updated", "item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item {item_id} deleted"}

@app.get("/redirect")
async def redirect():
    return {"message": "This should redirect to another URL"}, 301

@app.get("/server-error")
async def server_error():
    raise HTTPException(status_code=500, detail="Internal Server Error")
