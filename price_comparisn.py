import requests
from bs4 import BeautifulSoup
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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
        product_containers = soup.select('div.list-item')
        print('product_containers', product_containers)
        for container in product_containers:
            title = container.select_one('div.sku-list-item-price').text.strip()
            if product_name.lower() in title.lower():
                price = container.select_one('div.priceView-hero-price .priceView-customer-price span').text.strip()
                return f"Price on Bestbuy.com: {price}"

    elif 'walmart.com' in url:
        # Implement walmart.com scraping logic
        pass
    elif 'newegg.com' in url:
        # Implement newegg.com scraping logic
        pass
    
    return "Product not found"  # Default return value if the product is not found


def main():
    product_name = input("Enter the product name: ")
    
    bestbuy_url = f"https://www.bestbuy.com/site/searchpage.jsp?st={product_name.replace(' ', '+')}&intl=nosplash"
    walmart_url = f"https://www.walmart.com/search?q={product_name.replace(' ', '+')}"
    newegg_url = f"https://www.newegg.com/p/pl?d={product_name.replace(' ', '+')}"
    
    print(f"Searching for '{product_name}' on Bestbuy.com...")
    bestbuy_price = scrape_website(bestbuy_url, product_name)
    print(f"Price on Bestbuy.com: {bestbuy_price}")
    
    # print(f"Searching for '{product_name}' on Walmart.com...")
    # walmart_price = scrape_website(walmart_url, product_name)
    # print(f"Price on Walmart.com: {walmart_price}")
    
    # print(f"Searching for '{product_name}' on Newegg.com...")
    # newegg_price = scrape_website(newegg_url, product_name)
    # print(f"Price on Newegg.com: {newegg_price}")

if __name__ == "__main__":
    main()