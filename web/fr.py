"""
Parsing for French language grammar charts.
"""

from bs4 import BeautifulSoup


def parse(html: BeautifulSoup) -> str:
    """
    Parse HTML returned from web request for a French word.
    """
    all_tables = html.find_all("table")
    tables = [table for table in all_tables if table.select(".lang-fr") != []]

    html_str = ""
    if tables == []:
        plural_forms = html.select(".form-of.lang-fr")
        if plural_forms:
            html_str += ", ".join([form.text for form in plural_forms])
    else:
        html_str += "<br>".join(list(map(str, tables)))

    return html_str.replace("\n", "")
