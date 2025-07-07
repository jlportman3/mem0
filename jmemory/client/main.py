class APIError(Exception):
    """Exception raised for errors in the API."""

    pass


class MemoryClient:
    """Simplified client without telemetry."""

    def __init__(self, *args, **kwargs):
        pass


class AsyncMemoryClient:
    """Simplified async client without telemetry."""

    def __init__(self, *args, **kwargs):
        pass
