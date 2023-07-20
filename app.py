import requests
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/news', methods=['GET'])
def scrape_news():
    # URL of the news API endpoint
    url = 'https://newsapi.org/v2/everything?q=tesla&from=2023-07-01&sortBy=publishedAt&apiKey=87cd1114d2a6488c86a31ea3b3728107'

    # Send a GET request to the API
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    # Extract the articles from the response
    articles = data.get('articles', [])

    # Extract the title and description for each article
    news = []
    for article in articles:
        title = article.get('title', '')
        summary = article.get('description', '')
        news.append({'title': title, 'summary': summary})

    # Return the news as JSON
    return jsonify(news)

@app.route('/laptop_prices', methods=['GET'])
def scrape_laptop_prices():
    # URL of the Amazon laptops category
    url = 'https://www.amazon.com/s?k=laptops'

    # Send a GET request to the URL
    response = requests.get(url)

    # Create BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all laptop products on the page
    products = soup.find_all('div', {'class': 'sg-col-inner'})

    # List to store laptop details
    laptops = []

    # Extract details for each laptop
    for product in products:
        title_element = product.find('span', {'class': 'a-size-medium'})
        price_element = product.find('span', {'class': 'a-offscreen'})

        if title_element and price_element:
            title = title_element.text.strip()
            price = price_element.text.strip()

            laptops.append({
                'title': title,
                'price': price
            })

    # Return the scraped laptop data as JSON
    return jsonify(laptops)


if __name__ == '__main__':
    app.run(debug=True)


