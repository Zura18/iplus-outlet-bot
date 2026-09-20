import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

products = soup.select(".product-name")

print("iPlus Outlet პროდუქტები:")
print("-------------------------")

for product in products:
    name = product.get_text(strip=True)
    print(name)
