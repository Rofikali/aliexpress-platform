from opentelemetry import trace

tracer = trace.get_tracer("aliexpress-clone")

def start_span(name: str):
    return tracer.start_as_current_span(name)
