"""
Parsing for Romanian language grammar charts.
"""

from bs4 import BeautifulSoup


def parse(html: BeautifulSoup) -> str:
    """
    Parse HTML returned from web request for a Russian word.
    """
    all_tables = html.find_all("table", {"class": "inflection-table"})
    tables = [
        table
        for table in all_tables
        if table.select(".lang-ro") != [] or table.select('[lang="ro"]')
    ]
    html_str = "<br>".join(list(map(lambda html: str(html), tables)))

    verbs = html.find_all("table", {"class": "roa-inflection-table"})
    html_str += "<br>".join(list(map(lambda html: str(html), verbs)))

    return html_str.replace("\n", "")
