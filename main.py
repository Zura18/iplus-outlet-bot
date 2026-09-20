import requests
from bs4 import BeautifulSoup

url = "https://iplus.com.ge/ka/outlet/"

response = requests.get(url)

print("Status code:", response.status_code)
print("HTML length:", len(response.text))

soup = BeautifulSoup(response.text, "html.parser")

print("\nყველა ტექსტური ნაწილი:")
print("-------------------------")

for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5"]):
    text = tag.get_text(strip=True)

    if text:
        print(text)
