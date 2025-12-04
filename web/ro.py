"""
Parsing for Romanian language grammar charts.
"""

from bs4 import BeautifulSoup


def parse(html: BeautifulSoup) -> tuple[list[str], str]:
    """
    Parse HTML returned from web request for a Russian word.
    """
    header = html.find("h2", {"id": "Romanian"})
    nxt = header.parent.find_next_sibling()
    ipa = None
    while True:
        if nxt is not None:
            ipa = [str(tag.parent) for tag in nxt.find_all("span", {"class": "IPA"})]
            if ipa:
                break
            nxt = nxt.find_next_sibling()
        else:
            break

    all_tables = html.find_all("table", {"class": "inflection-table"})
    tables = [
        table
        for table in all_tables
        if table.select(".lang-ro") != [] or table.select('[lang="ro"]')
    ]
    html_str = "<br>".join(list(map(lambda html: str(html), tables)))

    verbs = html.find_all("table", {"class": "roa-inflection-table"})
    html_str += "<br>".join(list(map(lambda html: str(html), verbs)))

    return (ipa, html_str.replace("\n", ""))
