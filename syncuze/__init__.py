from syncuze.client import MemoryClient
from syncuze.direct import LocalMemoryClient

__version__ = "1.0.0"


def SyncUzeMemory(
    base_url: str = "http://localhost:8000",
    mode: str = "http",
    timeout: float = 30.0
):
    """
    Factory function for obtaining a SyncUze SDK client instance.
    
    :param base_url: The base URL of the FastAPI SyncUze backend (used if mode='http').
    :param mode: Execution mode, either 'http' (REST client) or 'local' (direct embedded DB calls).
    :param timeout: HTTP request timeout in seconds (used if mode='http').
    :return: MemoryClient instance if mode=='http', else LocalMemoryClient instance.
    """
    if mode.lower() == "local":
        return LocalMemoryClient()
    return MemoryClient(base_url=base_url, timeout=timeout)


__all__ = [
    "MemoryClient",
    "LocalMemoryClient",
    "SyncUzeMemory",
    "__version__",
]
