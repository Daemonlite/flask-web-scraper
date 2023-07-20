from flask import Flask, jsonify
from playwright.async_api import async_playwright, Error
from asyncio import gather

app = Flask(__name__)

async def get_stock(product_div):
    elements = await product_div.query_selector_all('.a-size-base')
    filtered_elements = [element for element in elements if 'stock' in await element.inner_text()]
    return filtered_elements

async def get_product(product_div):
    # Query for all elements at once
    image_element_future = product_div.query_selector('img.s-image')
    name_element_future = product_div.query_selector('h2 a span')
    price_element_future = product_div.query_selector('span.a-offscreen')
    url_element_future = product_div.query_selector('a.a-link-normal.s-no-hover.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')

    # Await all queries at once
    image_element, name_element, price_element, url_element = await gather(
        image_element_future,
        name_element_future,
        price_element_future,
        url_element_future,
        # get_stock(product_div)
    )

    # Fetch all attributes and text at once
    image_url = await image_element.get_attribute('src') if image_element else None
    product_name = await name_element.inner_text() if name_element else None
    try:
        product_price = float((await price_element.inner_text()).replace("$", "").replace(",", "").strip()) if price_element else None
    except:
        product_price = None
    product_url = "/".join((await url_element.get_attribute('href')).split("/")[:4]) if url_element else None

    return {"img": image_url, "name": product_name, "price": product_price, "url": product_url}

@app.route('/macbooks', methods=['GET'])
async def get_macbooks():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()

        url = 'https://www.amazon.ca/s?k=macbook'
        await page.goto(url)

        macbooks = []

        try:
            await page.wait_for_selector('.s-image')
            product_divs = await page.query_selector_all('.sg-col-inner')

            for product_div in product_divs:
                product_data = await get_product(product_div)
                macbooks.append(product_data)

        except Error:
            print('Timeout error occurred.')

        await browser.close()

        return jsonify(macbooks)

if __name__ == '__main__':
    app.run(debug=True)

