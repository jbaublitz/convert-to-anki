"""
Handles web scraping.
"""

import asyncio

import aiohttp
from bs4 import BeautifulSoup

from config import Entry
from web import fr, ru, uk, es

URL = "https://en.wiktionary.org/wiki/"


async def fetch(
    session: aiohttp.ClientSession, word: str, lang: str | None
) -> tuple[str, str] | None:
    """
    Fetch individual word asynchronously.
    """
    if lang is None:
        return None

    try:
        async with session.get(URL + word.replace("\u0301", "")) as response:
            if response.status == 404:
                return None
            text = await response.text()
            html = BeautifulSoup(text, "html.parser")

            if lang == "fr":
                return (word, fr.parse(html))
            if lang == "es":
                return (word, es.parse(html))
            if lang == "ru":
                return (word, ru.parse(html))
            if lang == "uk":
                return (word, uk.parse(html))

            return None
    except Exception as err:
        raise RuntimeError(f"Error fetching word {word}") from err


async def scrape(lang: str | None, words: list[Entry]) -> dict[str, str | None]:
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
