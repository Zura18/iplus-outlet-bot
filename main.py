import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

print("Status code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print("\nბმულები:")
print("-------------------------")

for link in soup.find_all("a"):
    name = link.get_text(" ", strip=True)

    if name:
        print(name)
