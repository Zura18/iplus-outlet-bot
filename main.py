import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

products = soup.select("a.product-title")

print("\nOutlet პროდუქტები:")
print("-------------------------")

for product in products:
    name = product.get_text(" ", strip=True)
    link = product.get("href")

    print("პროდუქტი:", name)
    print("ლინკი:", link)
    print("-------------------------")

print("სულ პროდუქტები:", len(products))
