import requests
from bs4 import BeautifulSoup
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
]

def scrape_website(url, product_name):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers)
    print('response', response)

    # Add a delay to make the requests seem more human-like
    time.sleep(random.uniform(2, 5))
    soup = BeautifulSoup(response.content, 'html.parser')
      
    if 'bestbuy.com' in url:
        # bestbuy.com scraping logic
        first_item = soup.find('li', class_='sku-item')

        # Find the div containing the price
        price_div = first_item.find('div', class_='priceView-customer-price')
        print('price_div', price_div)
        # Extract the price text
        price_span = price_div.find('span', attrs={'aria-hidden': 'true'})
        price = price_span.text
        return price
    
    elif 'walmart.com' in url:
       # Find the div containing the price
        first_item = soup.find('div', {'data-testid' : 'list-view'})
        print('first_item', first_item)
        price_div = first_item.find('div', {'data-automation-id': 'product-price'})
        
        current_price_element = price_div.find('span', class_='w_iUH7')
        print('current_price_element', current_price_element)
        # Extract the price text
        price = current_price_element.text
        return price

    elif 'newegg.com' in url:
        # newegg.com scraping logic
        first_item = soup.find('div', class_='item-container')
        print('first_item', first_item)
        # Find the div containing the price
        price_div = first_item.find('li', class_='price-current')
        print('price_div', price_div)
        # Extract the currency symbol
        currency_symbol = price_div.find('strong').previous_sibling.strip()
        print('currency_symbol', currency_symbol)
        # Extract the value before the dot
        price_integer = price_div.find('strong').get_text(strip=True)

        # Extract the value after the dot
        price_fraction = price_div.find('sup').get_text(strip=True)

        # Concatenate the currency symbol, value before the dot, and value after the dot
        price = f"{currency_symbol}{price_integer}{price_fraction}"

        # Print the current price
        print("Current price:", price)
        
        return price
       
    
    return "Product not found"  # Default return value if the product is not found

    
def main():
    product_name = input("Enter the product name: ")
    
    bestbuy_url = f"https://www.bestbuy.com/site/searchpage.jsp?st={product_name.replace(' ', '+')}&intl=nosplash"
    walmart_url = f"https://www.walmart.com/search?q={product_name.replace(' ', '+')}&intl=nosplash"
    newegg_url = f"https://www.newegg.com/p/pl?d={product_name.replace(' ', '+')}"
    
    # print(f"Searching for '{product_name}' on Bestbuy.com...")
    # bestbuy_price = scrape_website(bestbuy_url, product_name)
    # print(f"Price on Bestbuy.com: {bestbuy_price}")
    
    # print(f"Searching for '{product_name}' on Walmart.com...")
    # walmart_price = scrape_website(walmart_url, product_name)
    # print(f"Price on Walmart.com: {walmart_price}")
    
    print(f"Searching for '{product_name}' on Newegg.com...")
    newegg_price = scrape_website(newegg_url, product_name)
    print(f"Price on Newegg.com: {newegg_price}")

if __name__ == "__main__":
    main()