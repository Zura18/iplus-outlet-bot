import requests
from bs4 import BeautifulSoup

base_url = "https://iplus.com.ge/ka/outlet/"

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
    "1TB",
    "64 GB",
    "128 GB",
    "256 GB",
    "512 GB"
]

print("ჩვენთვის საინტერესო პროდუქტები")
print("========================================")

for page in range(1, 4):

    if page == 1:
        url = base_url
    else:
        url = f"{base_url}?page={page}"

    response = requests.get(url)

    print(f"\nგვერდი {page} | Status code: {response.status_code}")
    print("----------------------------------------")

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("a.product-title")

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
            print("----------------------------------------")
