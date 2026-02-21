"""
Parsing for Ukrainian language grammar charts.
"""

from bs4 import BeautifulSoup


def parse(html: BeautifulSoup) -> str:
    """
    Parse HTML returned from web request for a Russian word.
    """
    all_tables = html.find_all("table", {"class": "inflection-table"})
    tables = [table for table in all_tables if table.select(".lang-uk") != []]
    html_str = "<br>".join(list(map(lambda html: str(html), tables)))

    rows = []

    comparative = html.find_all(
        lambda tag: tag.name == "i" and "comparative" in tag.text
    )
    if comparative:
        rows.extend(
            [
                comp.find_next_sibling().text
                for comp in comparative
                if comp is not None
                and comp.find_next_sibling() is not None
                and comp.find_next_sibling()["lang"] == "uk"
            ]
        )

    superlative = html.find_all(
        lambda tag: tag.name == "i" and "superlative" in tag.text
    )
    if superlative:
        rows.extend(
            [
                sup.find_next_sibling().text
                for sup in superlative
                if sup is not None
                and sup.find_next_sibling() is not None
                and sup.find_next_sibling()["lang"] == "uk"
            ]
        )

    if rows:
        html_str += "<br>" + ", ".join(rows)

    return html_str.replace("\n", "")
