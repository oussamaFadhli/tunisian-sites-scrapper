import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode to not open a browser window
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL of the website with the search for "Ryzen 5 3400G"
url = "https://barbechli.tn/search;text=Ryzen 5 3400G;subcategories=components;availabilities=on_stock,on_command"

# Open the webpage
driver.get(url)

# Wait for the page to load completely (adjust the sleep time if needed)
time.sleep(5)

# Extract product details
products = []
product_cards = driver.find_elements(By.TAG_NAME, 'product-card')

for product in product_cards:
    try:
        name = product.find_element(By.CLASS_NAME, "ba-item-title").text
        price = product.find_element(By.CLASS_NAME, "size-medium").text
        image_url = product.find_element(By.CLASS_NAME, "card-img-top").get_attribute('src')
        
        products.append({
            "name": name,
            "price": price,
            "image_url": image_url
        })
    except Exception as e:
        print(f"Error extracting data for a product: {e}")

# Save the results to a JSON file
with open('Ryzen 5 3400G_products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=4)

# Close the driver
driver.quit()
