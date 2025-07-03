"""
Parsing for Russian language grammar charts.
"""

from bs4 import BeautifulSoup


def parse(html: BeautifulSoup) -> str:
    """
    Parse HTML returned from web request for a Russian word.
    """
    all_tables = html.find_all("table", {"class": "inflection-table"})
    tables = [table for table in all_tables if table.select(".lang-ru") != []]
    html_str = "<br>".join(list(map(lambda html: str(html), tables)))

    rows = []

    comparative = html.find_all("b", {"class": "comparative-form-of"})
    if comparative:
        rows.extend([comp.text for comp in comparative])

    superlative = html.find_all("b", {"class": "superlative-form-of"})
    if superlative:
        rows.extend([sup.text for sup in superlative])

    if rows:
        html_str += "<br>" + ", ".join(rows)

    return html_str.replace("\n", "")
