from bs4 import BeautifulSoup
import requests
from BooksToScrape import BooksToScrape
import time


if __name__ == "__main__":
    # Start time
    start_time = time.time()

    # URL of the website we want to scrape
    url = "https://books.toscrape.com/"

    # Send an HTTP GET request to retrieve the content of the specified URL as text
    result = requests.get(url).text
    soup = BeautifulSoup(result, "html.parser")

    # Initialize the parser class
    parser = BooksToScrape()

    # Get total number of result pages
    total_pages = parser.get_total_pages(soup)

    # Parse all the results
    results = parser.parse(int(total_pages))

    # Print results
    print(results)

    # Execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} sec!")
