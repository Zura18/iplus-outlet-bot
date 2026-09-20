import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

products = soup.select("a.product-title")

phone_brands = [
    "iPhone",
    "Samsung",
    "Google Pixel",
    "Xiaomi",
    "OnePlus",
    "Motorola"
]

laptop_brands = [
    "MacBook",
    "ASUS",
    "Lenovo",
    "HP",
    "Dell",
    "Acer",
    "MSI"
]

brands = phone_brands + laptop_brands

storage = [
    "64GB",
    "128GB",
    "256GB",
    "512GB",
    "1TB"
]

print("\nტელეფონები და ლეპტოპები:")
print("-------------------------")

for product in products:

    name = product.get_text(" ", strip=True)
    link = product.get("href")

    has_brand = any(
        brand.lower() in name.lower()
        for brand in brands
    )

    has_storage = any(
        size.lower() in name.lower()
        for size in storage
    )

    has_refurbished = "refurb" in name.lower()

    if has_brand and has_storage and has_refurbished:
        print("პროდუქტი:", name)
        print("ლინკი:", link)
        print("-------------------------")
