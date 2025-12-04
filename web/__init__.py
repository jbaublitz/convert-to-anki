"""
Handles web scraping.
"""

import os
import asyncio

import aiohttp
from bs4 import BeautifulSoup

from cache import add_to_cache, get_from_cache
from config import Entry
from web import fr, ro, ru, uk, es

URL = "https://en.wiktionary.org/wiki/"


async def fetch(
    session: aiohttp.ClientSession, word: str, lang: str | None
) -> tuple[str, str | tuple[str, str]] | None:
    """
    Fetch individual word asynchronously.
    """
    if lang is None:
        return None

    url = URL + word.replace("\u0301", "")
    cached = get_from_cache(url)
    if cached is None:
        print(f"Fetching html for URL {url}")
        user = os.environ["USER"]
        headers = {
            "User-Agent": f"convert-to-anki, user {user} (https://github.com/jbaublitz/convert-to-anki)"
        }
        async with session.get(url, headers=headers) as response:
            if response.status == 404:
                add_to_cache(url, "")
                return None
            if response.status != 200:
                raise RuntimeError(
                    f"Received HTTP code {response.status}: {response.reason}"
                )
            text = await response.text()
            add_to_cache(url, text)
    else:
        print(f"Getting cache for URL {url}")
        if cached == "":
            return None
        text = cached

    html = BeautifulSoup(text, "html.parser")

    if lang == "fr":
        return (word, fr.parse(html))
    if lang == "es":
        return (word, es.parse(html))
    if lang == "ro":
        return (word, ro.parse(html))
    if lang == "ru":
        return (word, ru.parse(html))
    if lang == "uk":
        return (word, uk.parse(html))

    return None


async def scrape(
    lang: str | None, words: list[Entry]
) -> dict[str, str | tuple[str, str]]:
    """
    Fetch all words asynchronously.
    """

    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(
            *[fetch(session, word.get_word(), lang) for word in words]
        )
        scraped_info = {}
        for tup_or_none in ret:
            if tup_or_none is not None:
                (word, info) = tup_or_none
                scraped_info[word] = info

        return scraped_info
