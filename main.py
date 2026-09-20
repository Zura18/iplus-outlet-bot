import requests
from bs4 import BeautifulSoup
import json
import os

base_url = "https://iplus.com.ge/ka/outlet/"
products_file = "products.json"

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


# უკვე ნანახი პროდუქტების წაკითხვა
if os.path.exists(products_file):
    with open(products_file, "r", encoding="utf-8") as file:
        old_products = json.load(file)
else:
    old_products = {}


current_products = {}


print("iPlus Outlet - შემოწმება")
print("========================================")


for page in range(1, 4):

    if page == 1:
        url = base_url
    else:
        url = f"{base_url}?page={page}"

    response = requests.get(url)

    print(f"\nგვერდი {page} | Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("a.product-title")

    for product in products:

        name = product.get_text(" ", strip=True)
        link = product.get("href")

        # თუ link სრული URL არ არის
        if link.startswith("/"):
            link = "https://iplus.com.ge" + link

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

            current_products[link] = {
                "name": name,
                "link": link
            }


# ახალი პროდუქტების მოძებნა
new_products = []

for link, product in current_products.items():

    if link not in old_products:
        new_products.append(product)


# შედეგის ჩვენება
print("\n----------------------------------------")
print(f"ნაპოვნია შესაბამისი პროდუქტები: {len(current_products)}")
print(f"ახალი პროდუქტები: {len(new_products)}")
print("----------------------------------------")


if new_products:

    print("\n🆕 ახალი პროდუქტები:")

    for product in new_products:

        print("პროდუქტი:", product["name"])
        print("ლინკი:", product["link"])
        print("----------------------------------------")

else:

    print("\nახალი პროდუქტები არ არის.")


# მიმდინარე პროდუქტების შენახვა
with open(products_file, "w", encoding="utf-8") as file:
    json.dump(current_products, file, ensure_ascii=False, indent=4)

print("\nშემოწმება დასრულდა.")
