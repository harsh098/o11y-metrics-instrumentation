from flask import Flask, jsonify, request, redirect
from werkzeug.exceptions import HTTPException
from opentelemetry import trace, metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import random

METRICS_FILE = open("./metrics_data.txt", mode="w", encoding="utf-8")

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

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the API"})

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    if item_id == 0:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"item_id": item_id, "name": f"Item {item_id}"})

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    if data.get("price", 0) <= 0:
        return jsonify({"error": "Price must be positive"}), 400
    return jsonify({"message": "Item created", "item": data})

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id == 0:
        return jsonify({"error": "Item not found"}), 404
    data = request.json
    if data.get("price", 0) <= 0:
        return jsonify({"error": "Price must be positive"}), 400
    return jsonify({"message": "Item updated", "item_id": item_id, "item": data})

@app.route("/items/<int:item_id>", methods=["PATCH"])
def partial_update_item(item_id):
    if item_id == 0:
        return jsonify({"error": "Item not found"}), 404
    data = request.json
    return jsonify({"message": "Item partially updated", "item_id": item_id, "item": data})

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id == 0:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": f"Item {item_id} deleted"})

@app.route("/redirect", methods=["GET"])
def handle_redirect():
    return redirect("/", code=301)

@app.route("/server-error", methods=["GET"])
def server_error():
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
