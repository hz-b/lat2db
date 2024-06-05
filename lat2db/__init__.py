from ._config import mongodb_url as _mongodb_url

mongodb_url = _mongodb_url(__name__)

__all__ = ["bl", "controller", "model", "mongodb_url"]
