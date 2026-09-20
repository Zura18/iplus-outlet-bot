import requests
from bs4 import BeautifulSoup
import json
import os

base_url = "https://iplus.com.ge/ka/outlet/"
products_file = "products.json"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

HEADERS = {"User-Agent": "Mozilla/5.0"}

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
    try:
        with open(products_file, "r", encoding="utf-8") as file:
            old_products = json.load(file)
    except json.JSONDecodeError:
        old_products = {}
else:
    old_products = {}


current_products = {}
had_error = False


print("iPlus Outlet - შემოწმება")
print("========================================")


for page in range(1, 4):

    if page == 1:
        url = base_url
    else:
        url = f"{base_url}?page={page}"

    try:
        response = requests.get(url, timeout=20, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"\nგვერდი {page} | შეცდომა: {e}")
        had_error = True
        continue

    print(f"\nგვერდი {page} | Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("a.product-title")

    for product in products:

        name = product.get_text(" ", strip=True)
        link = product.get("href")

        if not link:
            continue

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


# დაცვა: თუ არაფერი მოიძებნა ან რომელიმე გვერდი ჩავარდა,
# ძველ ფაილს არ ვშლით (თორემ შემდეგზე ყველაფერი "ახალი" გამოჩნდება)
if not current_products:
    print("პროდუქტები ვერ მოიძებნა, ფაილს არ ვცვლი.")
    raise SystemExit(0)


# ახალი პროდუქტების მოძებნა
new_products = []

for link, product in current_products.items():

    if link not in old_products:
        new_products.append(product)


print("\n----------------------------------------")
print(f"ნაპოვნია შესაბამისი პროდუქტები: {len(current_products)}")
print(f"ახალი პროდუქტები: {len(new_products)}")
print("----------------------------------------")


# Telegram შეტყობინება
if new_products:

    for product in new_products:

        message = (
            "🆕 ახალი ელემენტი დაემატა!\n\n"
            f"📱 {product['name']}\n\n"
            f"🔗 {product['link']}"
        )

        telegram_url = (
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        )

        telegram_data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        try:
            telegram_response = requests.post(
                telegram_url,
                data=telegram_data,
                timeout=20
            )
            sent = telegram_response.ok
            if not sent:
                print(telegram_response.text)
        except requests.RequestException as e:
            print(e)
            sent = False

        if sent:
            print("Telegram შეტყობინება გაიგზავნა ✅")
        else:
            print("Telegram შეცდომა ❌ (შემდეგ გაშვებაზე ისევ ცდის)")
            # არ ვინახავთ, რომ შემდეგ ჯერზე ისევ სცადოს
            current_products.pop(product["link"], None)

else:

    print("\nახალი პროდუქტები არ არის.")


# თუ რომელიმე გვერდი ჩავარდა, ძველი ჩანაწერები შევინარჩუნოთ
if had_error:
    current_products = {**old_products, **current_products}


# მიმდინარე პროდუქტების შენახვა
with open(products_file, "w", encoding="utf-8") as file:
    json.dump(current_products, file, ensure_ascii=False, indent=4)

print("\nშემოწმება დასრულდა.")
