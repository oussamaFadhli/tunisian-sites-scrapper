import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def setup_driver():
    """Setup Selenium WebDriver with Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Initialize the WebDriver with WebDriver Manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_amazon_products():
    """Scrape product details from all paginated Amazon search results."""
    url = "https://www.amazon.com/s?k=ryzen+5+3400G&crid=1ILATD90F2N42&sprefix=%2Caps%2C756&ref=nb_sb_ss_recent_1_0_recent"
    driver = setup_driver()
    driver.get(url)
    
    # Wait for the page to load completely
    time.sleep(5)
    
    products = []
    
    while True:
        try:
            # Wait for the main product grid to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
            )
            
            # Parse page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            items = soup.select('div.s-main-slot div.s-result-item[data-component-type="s-search-result"]')
            
            for item in items:
                try:
                    # Extract product title
                    title_element = item.select_one('h2 span')
                    title = title_element.text.strip() if title_element else None
                    
                    # Extract price
                    price_whole = item.select_one('span.a-price-whole')
                    price_fraction = item.select_one('span.a-price-fraction')
                    price = None
                    if price_whole:
                        price = f"{price_whole.text.strip()}.{price_fraction.text.strip() if price_fraction else '00'}"
                    
                    # Extract rating
                    rating_element = item.select_one('span.a-icon-alt')
                    rating = rating_element.text.split(' ')[0] if rating_element else None
                    
                    # Extract number of reviews
                    reviews_element = item.select_one('span.a-size-base.s-underline-text')
                    reviews = reviews_element.text.strip() if reviews_element else None
                    
                    # Extract product image URL
                    image_element = item.select_one('img.s-image')
                    image_url = image_element['src'] if image_element else None
                    
                    # Append product data
                    if title:
                        products.append({
                            "title": title,
                            "price": price,
                            "rating": rating,
                            "reviews": reviews,
                            "image_url": image_url,
                        })
                except Exception as e:
                    print(f"Error extracting a product: {e}")
            
            # Find and click the "Next" button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
                if "s-pagination-disabled" in next_button.get_attribute("class"):
                    break  # Exit loop if "Next" button is disabled (last page)
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
            except Exception as e:
                print(f"No more pages: {e}")
                break  # Exit loop if "Next" button is not found
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            break
    
    driver.quit()
    return products

def save_to_json(products):
    """Save product data to a JSON file."""
    with open('amazon_products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    products = scrape_amazon_products()
    save_to_json(products)
    print(f"Scraped {len(products)} products successfully!")
