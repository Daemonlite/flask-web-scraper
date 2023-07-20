import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.google.com/search?q=discounted+laptops&oq=discounted+laptops'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
data = requests.get(url, headers=header)

if data.status_code == 200:
    soup = BeautifulSoup(data.content, "html.parser")
    results = []
    for g in soup.find_all('div', {'class': 'g'}):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            try:
                description = g.find('div', {'data-sncf': '2'}).text
            except Exception as e:
                description = "-"

            # Extract discounted price from the description using regular expressions
            # Hypothetical example: Assuming the price is in the format $XXX.XX
            price_match = re.search(r'\$\d+\.\d+', description)
            price = price_match.group() if price_match else "N/A"

            results.append(f"{price};{link};{description}")

with open("discounted_laptops.csv", "w") as f:
    f.write("Price; Link; Description\n")

for result in results:
    with open("discounted_laptops.csv", "a", encoding="utf-8") as f:
        f.write(str(result) + "\n")

