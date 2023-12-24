from decimal import Decimal
import time
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

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
                    "description": description,
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

@app.route('/laptops')
def get_laptop_prices():
    url = 'https://www.google.com/search?q=laptop+prices&oq=laptop+prices'
    results = scrape_google_search_results(url)
    if results is not None:
        return jsonify(results)
    else:
        return jsonify({"message": "Failed to fetch laptop prices."}), 500
    
@app.route('/cheap-laptops')
def scrape_laptops():
    url = "https://www.theverge.com/22652565/best-cheap-laptops"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data'})

    soup = BeautifulSoup(response.text, 'html.parser')
    laptops = []

    laptop_elements = soup.select('.duet--article--product-card')
    for laptop_elem in laptop_elements:
        name_elem = laptop_elem.select_one('h3 a')
        price_elem = laptop_elem.select_one('span.text-18')
        specs_elem = laptop_elem.select_one('p.font-fkroman')

        if name_elem and price_elem and specs_elem:
            name = name_elem.get_text(strip=True)
            price = price_elem.get_text(strip=True)
            specs = specs_elem.get_text(strip=True)
            laptops.append({'name': name, 'price': price, 'specs': specs})

    return jsonify(laptops)

#scrape from compu ghana
@app.route('/compu-ghana')
def scrape_laptop_data():
    url = "https://compughana.com/it-networking/laptops.html?&price=-10000"  
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    laptops = []

    for laptop_item in soup.find_all("div", class_="product-item-details"):
        name = laptop_item.find("strong", class_="product-item-name").text.strip()
        price = laptop_item.find("span", class_="price").text.strip()

        laptops.append({"name": name, "price": price})

    return jsonify(laptops)



@app.route('/get4less')
def get_laptop_data():
    url = "https://get4lessghana.com/product-category/it-products/computer/laptop/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    laptops = []

    for laptop_item in soup.find_all("li", class_="rey-swatches"):
        name = laptop_item.find("h2", class_="woocommerce-loop-product__title").text.strip()
        price = laptop_item.find("span", class_="woocommerce-Price-amount").text.strip()

        laptops.append({"name": name, "price": price})

    return jsonify(laptops)



@app.route('/rental', methods=['GET'])
def get_property_listings():
    url = 'https://www.realtor.com/international/gh/rent?sort=price+asc'

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    property_listings = []

    for property_div in soup.find_all('a', class_='sc-1dun5hk-0 cOiOrj'):
        img_src = property_div.find('img')['src']
        price = property_div.find('div', class_='displayConsumerPrice').text.strip()
        address = property_div.find('div', class_='address').text.strip()
        property_type = property_div.find('div', class_='property-type').text.strip()
        view_details_link = property_div['href']

        property_info = {
            'img_src': img_src,
            'price': price,
            'address': address,
            'property_type': property_type,
            'view_details_link': view_details_link,
        }

        property_listings.append(property_info)


    return jsonify(property_listings)
        
@app.route('/educational_tours', methods=['GET'])
def get_educational_tours():

    url = 'https://www.tourradar.com/o/olives-travel-tour-ghana/tours'

  
    response = requests.get(url)
    html = response.text

 
    soup = BeautifulSoup(html, 'html.parser')

    educational_tours = []

    for tour_div in soup.find_all('li', class_='js-ao-serp-tour-card ao-serp-tour-card'):
        title = tour_div.find('h4', class_='js-ao-serp-tour__name ao-serp-tour-card__title').text.strip()
        image_src = tour_div.find('img', class_='ao-serp-tour-card__hero-image')['src']
        duration = tour_div.find('dd', class_='ao-serp-tour-card__detail-value').text.strip()
        price = tour_div.find('dd', class_='ao-serp-tour-card__detail-value--price').text.strip()
        operator = tour_div.find('dd', class_='ao-serp-tour-card__values-content--operator').text.strip()
        view_tour_link = tour_div.find('a', class_='ao-serp-tour-card__button')['href']

        tour_info = {
            'title': title,
            'image_src': image_src,
            'duration': duration,
            'price': price,
            'operator': operator,
            'view_tour_link': f"https://www.tourradar.com{view_tour_link}",
        }

        educational_tours.append(tour_info)

    return jsonify(educational_tours)

if __name__ == '__main__':
    app.run(debug=True)