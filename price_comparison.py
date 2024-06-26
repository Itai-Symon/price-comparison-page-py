import requests
from bs4 import BeautifulSoup
import random
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
]

app = FastAPI()

# Allow requests from the Next.js frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def scrape_website(url, product_name):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers)
    print('response', response)

    # Add a delay to make the requests seem more human-like
    time.sleep(random.uniform(2, 5))
    soup = BeautifulSoup(response.content, 'html.parser')
      
    if 'bestbuy.com' in url:
        # bestbuy.com scraping logic
        items = soup.find_all('li', class_='sku-item')
        for first_item in items:
            try:
                # Find the div containing the price
                price_div = first_item.find('div', class_='priceView-customer-price')
                print('price_div', price_div)
                # Extract the price text
                price_span = price_div.find('span', attrs={'aria-hidden': 'true'})
                price = price_span.text

                # Extract the URL of the chosen product
                url_container = first_item.find('h4', class_='sku-title')
                if not url_container:
                    if first_item.find('h4', class_='sku-header'):
                        url_container = first_item.find('h4', class_='sku-header')
                    else:
                        url_container = first_item.find('div', class_='sku-title')
                print('url_container', url_container)
                url = f'https://www.bestbuy.com/{url_container.find('a').get('href')}'
                if not url.startswith('https://'):
                    url = f'https://www.bestbuy.com{url}'
                print('bestbuy url', url)

                return price, url
            
            except Exception as e:
                print('Error:', e)
                continue
    
    elif 'walmart.com' in url:
       # Find the div containing the price
        first_item = soup.find('div', {'data-testid' : 'list-view'})
        print('first_item', first_item)
       
        # Find the sibling containing the URL
        url_element = first_item.find_previous_sibling('a', {'link-identifier': True})
        print('url_element', url_element)
        
        url = url_element.get('href')

        if not url.startswith('https://'):
            url = f'https://www.walmart.com{url_element.get("href")}'
        # Extract the URL from the href attribute

        price_div = first_item.find('div', {'data-automation-id': 'product-price'})
        
        current_price_element = price_div.find('span', class_='w_iUH7')
        print('current_price_element', current_price_element)
        # Extract the price text
        price_text = current_price_element.text.strip()
        price = price_text.split('$')[-1].strip()
        price = f"${price}"
        return price, url

    elif 'newegg.com' in url:
        # newegg.com scraping logic
        item_cells = soup.find_all('div', class_='item-cell')
        
        for item_cell in item_cells:
            try:
                first_item = item_cell.find('div', class_='item-container')
                print('first_item', first_item)
                # Find the div containing the price
                price_div = first_item.find('li', class_='price-current')
                print('price_div', price_div)
                # Extract the currency symbol
                currency_symbol = price_div.find('strong').previous_sibling.strip()
                
                # Extract the value before the dot
                price_integer = price_div.find('strong').get_text(strip=True)

                # Extract the value after the dot
                price_fraction = price_div.find('sup').get_text(strip=True)

                # Concatenate the currency symbol, value before the dot, and value after the dot
                price = f"{currency_symbol}{price_integer}{price_fraction}"

                # Extract the URL of the chosen product
                url = first_item.find('a', class_='item-title').get('href')
                if not url.startswith('https://'):
                    url = f'https://www.newegg.com{url}'
                print('newegg url', url)
                
                return price, url
            
            except Exception as e:
                print('Error:', e)
                continue

        return None, None
       
    return "Product not found"  # Default return value if the product is not found

@app.get("/search")
def search_product(product_name: Optional[str] = None):
    if not product_name:
        return {"error": "product_name is required"}
    
    bestbuy_url = f"https://www.bestbuy.com/site/searchpage.jsp?st={product_name.replace(' ', '+')}&intl=nosplash"
    walmart_url = f"https://www.walmart.com/search?q={product_name.replace(' ', '+')}&intl=nosplash"
    newegg_url = f"https://www.newegg.com/p/pl?d={product_name.replace(' ', '+')}"
    
    print(f"Searching for '{product_name}' on Bestbuy.com...")
    bestbuy_price, bestbuy_chosen_product_url = scrape_website(bestbuy_url, product_name)
    print(f"Price on Bestbuy.com: {bestbuy_price}")
    
    print(f"Searching for '{product_name}' on Walmart.com...")
    walmart_price, walmart_chosen_product_url = scrape_website(walmart_url, product_name)
    print(f"Price on Walmart.com: {walmart_price}")
    
    print(f"Searching for '{product_name}' on Newegg.com...")
    newegg_price, newegg_chosen_product_url = scrape_website(newegg_url, product_name)
    print(f"Price on Newegg.com: {newegg_price}")

    return {
        "product_name": product_name,
        "bestbuy_chosen_product_url": bestbuy_chosen_product_url,
        "bestbuy_price": bestbuy_price,
        "walmart_chosen_product_url": walmart_chosen_product_url,
        "walmart_price": walmart_price,
        "newegg_price": newegg_price,
        "newegg_chosen_product_url": newegg_chosen_product_url
    }



