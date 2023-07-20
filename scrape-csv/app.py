import requests
from bs4 import BeautifulSoup

url = 'https://www.google.com/search?q=cafe+in+new+york'
header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
data = requests.get(url, headers=header)

if data.status_code == 200:
    soup = BeautifulSoup(data.content, "html.parser")
    results = []
    for g in soup.find_all('div',  {'class':'g'}):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            try:
                description = g.find('div', {'data-sncf':'2'}).text
            except Exception as e:
                description = "-"
            results.append(str(title)+";"+str(link)+';'+str(description))

with open("cafes.csv", "w") as f:
    f.write("Title; Link; Description\n")

for result in results:
    with open("cafes.csv", "a", encoding="utf-8") as f:
        f.write(str(result)+"\n")
