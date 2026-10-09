"""Resolve bundled resource paths relative to the installed package,
so NLPyPort works regardless of the current working directory."""
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parent


def resource(relative_path):
	"""Return an absolute Path for a resource path given relative to the package dir."""
	return PKG_DIR / str(relative_path).strip()
