import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def get_page(page):
    try:
        url = BASE_URL.format(page)
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return None

def clean_price(price):
    return price.replace("Â", "").strip()

def scrape_books():
    all_books = []

    for page in range(1, 6): 
        soup = get_page(page)
        if not soup:
            continue

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            try:
                title = book.find("h3").find("a")["title"]
                price = clean_price(book.find("p", class_="price_color").text)
                availability = book.find("p", class_="instock availability").text.strip()

                all_books.append([title, price, availability])
            except Exception as e:
                print("Error extracting book:", e)

    return all_books

def save_to_csv(data):
    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Price", "Availability"])
        writer.writerows(data)

def main():
    print("Scraping started...")
    data = scrape_books()
    save_to_csv(data)
    print(f"Scraping completed. {len(data)} records saved.")

if __name__ == "__main__":
    main()