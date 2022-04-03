try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

from .main import create_app

__version__ = importlib_metadata.version(__name__)

app = create_app()
