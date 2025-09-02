"""
Handle HTML caching.
"""

import os
import hashlib


def add_to_cache(url: str, html: str):
    """
    Add an entry to the cache.
    """
    home = os.environ["HOME"]
    cache_path = os.path.join(home, ".local", "state", "convert-to-anki", "cache")
    os.makedirs(cache_path, exist_ok=True)

    hsh = hashlib.sha256(url.encode("utf-8")).hexdigest()
    with open(os.path.join(cache_path, f"{hsh}.txt"), "w", encoding="utf-8") as f:
        f.write(html)
        f.flush()


def get_from_cache(url: str) -> str | None:
    """
    Get an HTML entry from the cache or return None.
    """
    home = os.environ["HOME"]
    cache_path = os.path.join(home, ".local", "state", "convert-to-anki", "cache")

    hsh = hashlib.sha256(url.encode("utf-8")).hexdigest()
    try:
        with open(os.path.join(cache_path, f"{hsh}.txt"), "r", encoding="utf-8") as f:
            html = f.read()
            return html
    except FileNotFoundError:
        return None
