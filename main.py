import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\n17 Pro Max პროდუქტები:")
print("-------------------------")

for link in soup.find_all("a"):

    name = link.get_text(" ", strip=True)

    if "17 Pro Max" in name:
        print("პროდუქტი:", repr(name))
        print("ლინკი:", link.get("href"))
        print("-------------------------")
