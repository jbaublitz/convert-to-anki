"""
Parsing for Spanish language grammar charts.
"""

from bs4 import BeautifulSoup


def parse(html: BeautifulSoup) -> str:
    """
    Parse HTML returned from web request for a French word.
    """
    all_tables = html.find_all("table")
    tables = [table for table in all_tables if table.select(".lang-es") != []]

    html_str = ""
    if tables == []:
        adj_forms = html.select(".form-of.lang-es")
        if adj_forms:
            html_str += ", ".join([form.text for form in adj_forms])
    else:
        html_str += "<br>".join(list(map(lambda html: str(html), tables)))

    return html_str.replace("\n", "")
