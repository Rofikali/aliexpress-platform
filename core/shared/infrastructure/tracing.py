# # filename : core/shared/infrastructure/tracing.py

# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
#     OTLPSpanExporter,
# )


# def setup_tracing() -> None:
#     provider = TracerProvider()
#     trace.set_tracer_provider(provider)

#     exporter = OTLPSpanExporter(
#         endpoint="http://otel-collector:4317",
#         insecure=True,
#     )

#     processor = BatchSpanProcessor(exporter)
#     provider.add_span_processor(processor)


# tracer = trace.get_tracer("aliexpress-clone")


# def start_span(name: str):
#     return tracer.start_as_current_span(name)

# below is new code and above is old code

# from opentelemetry import trace
# from opentelemetry.trace import SpanContext


# tracer = trace.get_tracer("aliexpress-clone")


# def start_span(name: str):
#     """
#     Infra-safe span starter.
#     """
#     return tracer.start_as_current_span(name)


# def get_trace_id() -> str | None:
#     """
#     Returns current trace_id as hex string.
#     Safe for Kafka / logs / envelopes.
#     """
#     span = trace.get_current_span()
#     if not span:
#         return None

#     ctx: SpanContext = span.get_span_context()
#     if not ctx or not ctx.is_valid:
#         return None

#     return format(ctx.trace_id, "032x")


# filename: core/shared/infrastructure/tracing.py

from opentelemetry import trace
from opentelemetry.trace import SpanContext

_tracer = trace.get_tracer("aliexpress-clone")


def start_span(name: str):
    """
    Infra-safe span starter.
    No exporters. No providers. No side effects.
    """
    return _tracer.start_as_current_span(name)


def get_trace_id() -> str | None:
    """
    Returns current trace_id as hex string.
    Safe for Kafka, logs, envelopes.
    """
    span = trace.get_current_span()
    if not span:
        return None

    ctx: SpanContext = span.get_span_context()
    if not ctx or not ctx.is_valid:
        return None

    return format(ctx.trace_id, "032x")
