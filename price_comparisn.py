import requests
from bs4 import BeautifulSoup

def scrape_website(url, product_name):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Add website-specific logic to find the product price
    if 'bestbuy.com' in url:
        # Implement bestbuy.com scraping logic
        pass
    elif 'walmart.com' in url:
        # Implement walmart.com scraping logic
        pass
    elif 'newegg.com' in url:
        # Implement newegg.com scraping logic
        pass
    
    return "Product not found"  # Default return value if the product is not found

def main():
    product_name = input("Enter the product name: ")
    
    bestbuy_url = f"https://www.bestbuy.com/site/searchpage.jsp?st={product_name.replace(' ', '+')}"
    walmart_url = f"https://www.walmart.com/search?q={product_name.replace(' ', '+')}"
    newegg_url = f"https://www.newegg.com/p/pl?d={product_name.replace(' ', '+')}"
    
    print(f"Searching for '{product_name}' on Bestbuy.com...")
    bestbuy_price = scrape_website(bestbuy_url, product_name)
    print(f"Price on Bestbuy.com: {bestbuy_price}")
    
    print(f"Searching for '{product_name}' on Walmart.com...")
    walmart_price = scrape_website(walmart_url, product_name)
    print(f"Price on Walmart.com: {walmart_price}")
    
    print(f"Searching for '{product_name}' on Newegg.com...")
    newegg_price = scrape_website(newegg_url, product_name)
    print(f"Price on Newegg.com: {newegg_price}")

if __name__ == "__main__":
    main()