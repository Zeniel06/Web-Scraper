from bs4 import BeautifulSoup
import requests
import pandas as pd
current_page = 1

data = []

key = True

while (key):
    print(f"Currently scraping page: {current_page}")

    url="https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

# Note that this only scrapes for one page
    if soup.title.text == "404 Not Found":
        key = False
# This loop iterates over all the books/item on page 1
    else:
        all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for book in all_books:
            item = {}
            item["Title"] = book.find("img").attrs["alt"]
            item["Link"] = book.find("a").attrs["href"]
            item["Price"] = book.find("p", class_="price_color").text[2:]
            item["Stock"] = book.find("p", class_="instock availability").text.strip()

            data.append(item)

    current_page = current_page + 1 # Move onto the next page after completion

#convert the scraped data into excel file
df = pd.DataFrame(data)
df.to_excel("test.xlsx", index=False)