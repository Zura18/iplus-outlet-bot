import requests
from bs4 import BeautifulSoup

base_url = "https://iplus.com.ge/ka/outlet/"

for page in range(1, 4):

    if page == 1:
        url = base_url
    else:
        url = f"{base_url}?page={page}"

    response = requests.get(url)

    print("\n========================================")
    print(f"გვერდი {page}")
    print(f"URL: {url}")
    print(f"Status code: {response.status_code}")
    print("========================================")

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("a.product-title")

    print(f"პროდუქტების რაოდენობა: {len(products)}")
    print("----------------------------------------")

    for product in products:

        name = product.get_text(" ", strip=True)
        link = product.get("href")

        print("პროდუქტი:", name)
        print("ლინკი:", link)
        print("----------------------------------------")
