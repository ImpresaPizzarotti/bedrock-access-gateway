import os

API_ROUTE_PREFIX = os.environ.get("API_ROUTE_PREFIX", "/api/v1")

TITLE = "Amazon Bedrock Proxy APIs"
SUMMARY = "OpenAI-Compatible RESTful APIs for Amazon Bedrock"
VERSION = "0.1.0"
DESCRIPTION = """
Use OpenAI-Compatible RESTful APIs for Amazon Bedrock models.
"""

LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")
DEFAULT_EMBEDDING_MODEL = os.environ.get("DEFAULT_EMBEDDING_MODEL", "cohere.embed-multilingual-v3")
ENABLE_CROSS_REGION_INFERENCE = os.environ.get("ENABLE_CROSS_REGION_INFERENCE", "true").lower() != "false"
ENABLE_APPLICATION_INFERENCE_PROFILES = os.environ.get("ENABLE_APPLICATION_INFERENCE_PROFILES", "true").lower() != "false"
ENABLE_PROMPT_CACHING = os.environ.get("ENABLE_PROMPT_CACHING", "false").lower() != "false"
INFERENCE_PROFILE_REGEX_FILTER = os.environ.get("INFERENCE_PROFILE_REGEX_FILTER", "")

# Open Telemetry Settings
ENABLE_TRACING = os.environ.get("ENABLE_TRACING", "false").lower() == "true"
OTEL_EXPORTER_OTLP_ENDPOINT = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
OTEL_SERVICE_NAME = os.environ.get("OTEL_SERVICE_NAME", "bedrock-access-gateway")
OTEL_TRACES_SAMPLER = os.environ.get("OTEL_TRACES_SAMPLER", "traceidratio")
OTEL_TRACES_SAMPLER_ARG = float(os.environ.get("OTEL_TRACES_SAMPLER_ARG", "0.3"))