import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag

from collections import deque

SEED_URL = "https://testingurl.dev/scraping/links/circular"

def crawler(seed):
    frontier = deque([seed])
    seen = {seed}

    while frontier:
        url = frontier.pop()

        try:
            response = requests.get(url, timeout = 5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Request failed:", url, error)
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        h1 = soup.find("h1")

        if h1:
            print(h1.get_text())

        links = []

        for tag in soup.find_all("a", href=True):
            link = urljoin(response.url, tag["href"])

            link = urldefrag(link)[0]

            if link.startswith(seed):
                links.append(link)

        links.sort()

        for link in links:
            if link not in seen:
                seen.add(link)
                frontier.append(link)

    print("All URLs in seen:")
    for url in sorted(seen):
        print(url)

crawler("https://testingurl.dev/scraping/links/circular")

