import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

brands = [
    "iPhone",
    "Samsung",
    "Google",
    "Xiaomi",
    "OnePlus",
    "MacBook",
    "ASUS",
    "Lenovo",
    "HP",
    "Dell",
    "Acer",
    "MSI"
]

storage = [
    "64GB",
    "128GB",
    "256GB",
    "512GB",
    "1TB"
]

print("\nჩვენთვის საინტერესო პროდუქტები:")
print("-------------------------")

for link in soup.find_all("a"):

    name = link.get_text(" ", strip=True)

    if not name:
        continue

    has_brand = any(brand.lower() in name.lower() for brand in brands)
    has_storage = any(size.lower() in name.lower() for size in storage)
    has_refurbished = "refurb" in name.lower()

    if has_brand and has_storage and has_refurbished:
        print(name)
