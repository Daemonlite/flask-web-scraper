from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_google_search_results(url):
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
                results.append({
                    "title": title,
                    "link": link,
                    "description": description
                })

        return results
    else:
        return None

@app.route('/cafes')
def get_cafes_in_new_york():
    url = 'https://www.google.com/search?q=cafe+in+new+york'
    results = scrape_google_search_results(url)
    if results is not None:
        return jsonify(results)
    else:
        return jsonify({"message": "Failed to fetch cafes in New York."}), 500

@app.route('/laptop-prices')
def get_laptop_prices():
    url = 'https://www.google.com/search?q=laptop+prices&oq=laptop+prices'
    results = scrape_google_search_results(url)
    if results is not None:
        return jsonify(results)
    else:
        return jsonify({"message": "Failed to fetch laptop prices."}), 500

if __name__ == '__main__':
    app.run(debug=True)
