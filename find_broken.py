import requests
import sys
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlsplit, urljoin

# Status codes that indicate bad links
NOT_OK = [400, 404, 403, 408, 409, 501, 502, 503]
# Valid tag and attribute mappings
TAGS = {"a": "href", "img": "src", "script": "src", "link": "href"}

broken_links = []
visited_links = []


def generate_report(result, visited_links):
    report = "---\ntitle: Broken Link Report"
    report += "\nchecked: " + str(len(visited_links))
    report += "\nbroken: " + str(len(broken_links))
    report += "\n---\n"
    sorted_list = sorted(broken_links, key=lambda k: k['code'])
    for link in sorted_list:
        try:
            report += f"\n- code:    {link['code']}\n  url:     {link['link']}\n  parent:  {link['parent']}\n  error:   {link['err']}\n"
        except KeyError:
            report += f"\n- code:    {link['code']}\n  url:     {link['link']}\n  parent:  {link['parent']}\n"
    return report


def check_link(link, parent):
    try:
        r = requests.get(link)
        result = {"code": r.status_code, "link": link, "parent": parent}
        if result["code"] in NOT_OK:
            broken_links.append(result)
    except Exception as e:
        result = {"code": 0, "link": link, "parent": parent, "err": str(e)}
        broken_links.append(result)


def get_page(url, visited_links):
    response = requests.get(url)
    if url not in visited_links:
        visited_links.append(url)
    for tag, field in iter(TAGS.items()):
        try:
            # Find all the links on the page
            for tag_elem in BeautifulSoup(
                response.text, "html.parser", parse_only=SoupStrainer(tag)
            ):
                # Try to visit all the links on the page
                # No need to check elements without actual links
                if tag_elem.has_attr(field):
                    link = tag_elem.get(field)

                    # NOTE: urljoin() does not alter absolute URLs but does fix relative URLs
                    full_link = urljoin(url, link)

                    # Add link to visited list
                    if full_link not in visited_links:
                        visited_links.append(full_link)
                        check_link(full_link, url)
                        # If the visited link is in the domain, get all the links on it too
                        if urlsplit(full_link).netloc == url_domain:
                            get_page(full_link, visited_links)
        except Exception:
            pass
    finished_report = generate_report(broken_links, visited_links)
    return finished_report


if __name__ == "__main__":
    url = sys.argv[1]

    url_domain = urlsplit(url).netloc
    finished_report = get_page(url, visited_links)
    print(finished_report)

    sys.exit()
