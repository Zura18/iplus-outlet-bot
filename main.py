import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# ვეძებთ გვერდზე სიტყვას "Refurbrished"
products = soup.find_all(string=lambda text: text and "Refurbrished" in text)

print("\nRefurbrished პროდუქტების რაოდენობა:", len(products))
print("-------------------------")

for product in products:
    print("ნაპოვნია:", repr(product.strip()))

    parent = product.parent

    print("Parent tag:", parent.name)
    print("Parent class:", parent.get("class"))
    print("Parent id:", parent.get("id"))

    print("-------------------------")
