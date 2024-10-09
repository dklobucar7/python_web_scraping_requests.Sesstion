import requests
from bs4 import BeautifulSoup
import re


class BooksToScrape:
    def __init__(self):
        self.results = []
        self.session = requests.Session()  # Kreiramo session objekt

    def get_total_pages(self, soup):
        current_page_info = soup.find("li", {"class": "current"})
        if current_page_info:
            total_pages = int(current_page_info.text.strip().split(" ")[-1])
            return total_pages
        else:
            return 1

    def fetch_page(self, page_num):
        # Fetch the page for given page number
        url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
        page = self.session.get(url).text
        return BeautifulSoup(page, "html.parser")

    def extract_book_info(self, item):
        # Extract book information from the item element
        title = item.find("h3").find("a").text
        # price
        price_tag = item.find("p", {"class": "price_color"}).text
        price = float(re.sub(r"[^\d.]", "", price_tag))  # Cleaning the price

        # Check stock availability
        stock_tag = (
            item.find("p", {"class": "instock availability"}).text.strip().lower()
        )
        stock = 1 if stock_tag == "in stock" else 0

        # Extract book rating
        rating_tag = item.find("p", {"class": "star-rating"})["class"][1]
        rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        rating = rating_map.get(rating_tag, 0)

        # Return a dictionary with the book information
        return {"title": title, "price": price, "stock": stock, "rating": rating}

    def parse(self, total_pages):
        # Parse all the pages
        for page_num in range(1, total_pages + 1):
            doc = self.fetch_page(page_num)
            list_items = doc.find_all(
                "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"}
            )

            for item in list_items:
                self.results.append(self.extract_book_info(item))

        return self.results
