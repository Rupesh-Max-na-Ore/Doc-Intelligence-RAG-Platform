import requests
from bs4 import BeautifulSoup


BASE_URL = "http://books.toscrape.com/"


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def get_book_links():
    html = fetch_page(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")

    books = soup.select("article.product_pod h3 a")

    links = []
    for book in books:
        href = book.get("href")
        links.append(BASE_URL + href)

    return links