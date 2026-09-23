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
    html_str = "<br>".join(list(map(str, tables)))

    rows = []

    comparative = html.find_all("b", {"class": "comparative-form-of"})
    if comparative:
        rows.extend([comp.text for comp in comparative])

    superlative = html.find_all("b", {"class": "superlative-form-of"})
    if superlative:
        rows.extend([sup.text for sup in superlative])

    relational_adjective = html.find_all(
        lambda tag: tag.name == "i" and "relational adjective" in tag.text
    )
    if relational_adjective:
        rows.extend(
            [
                rel_adj.find_next_sibling().text
                for rel_adj in relational_adjective
                if rel_adj is not None
                and rel_adj.find_next_sibling() is not None
                and rel_adj.find_next_sibling().get("lang", None) == "ru"
            ]
        )

    if rows:
        html_str += "<br>" + ", ".join(rows)

    return html_str.replace("\n", "")
