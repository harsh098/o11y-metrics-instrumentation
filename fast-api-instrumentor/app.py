from fastapi import FastAPI
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

# Initialize FastAPI app
app = FastAPI()

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)



@app.on_event("shutdown")
def shutdown_event():
    if not METRICS_FILE.closed:
        METRICS_FILE.close()
    else:
        pass

@app.get("/health", status_code=201)
async def health():
    asyncio.sleep(random.randint(1,5))
    return {"message": "Hi Mom!"}

