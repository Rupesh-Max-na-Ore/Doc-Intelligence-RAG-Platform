from bs4 import BeautifulSoup


def parse_book(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1").text.strip()

    description_tag = soup.select_one("#product_description ~ p")
    description = description_tag.text.strip() if description_tag else ""

    rating_class = soup.select_one(".star-rating")["class"]
    rating = rating_class[1]  # e.g. "Three"

    return {
        "title": title,
        "description": description,
        "rating": rating,
        "url": url,
    }