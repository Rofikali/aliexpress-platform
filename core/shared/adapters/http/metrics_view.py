from prometheus_client import generate_latest
from django.http import HttpResponse


def metrics_view(request):
    return HttpResponse(
        generate_latest(),
        content_type="text/plain",
    )
