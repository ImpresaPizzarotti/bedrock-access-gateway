# import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.boto3sqs import Boto3SQSInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from api.setting import ENABLE_TRACING, OTEL_EXPORTER_OTLP_ENDPOINT, OTEL_SERVICE_NAME, OTEL_TRACES_SAMPLER_ARG

def setup_tracing():
    if not ENABLE_TRACING:
        return
    
    # Configure resource
    resource = Resource.create({"service.name": OTEL_SERVICE_NAME})
    
    # Configure sampler
    sampler = TraceIdRatioBased(OTEL_TRACES_SAMPLER_ARG)
    
    # Set up tracer provider
    trace.set_tracer_provider(TracerProvider(resource=resource, sampler=sampler))
    
    # Configure OTLP exporter
    otlp_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Auto-instrument libraries
    RequestsInstrumentor().instrument()
    Boto3SQSInstrumentor().instrument()

def instrument_fastapi(app):
    if ENABLE_TRACING:
        FastAPIInstrumentor.instrument_app(app)
