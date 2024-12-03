from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import time

def get_table_content():
    # Initialize Chrome driver
    driver = webdriver.Chrome()
    
    try:
        # Load the page
        driver.get("https://pcbuilder.net/product/processor/")
        
        # Wait for Cloudflare challenge to complete and myTable to be present
        table = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "myTable"))
        )
        
        # Get the table content
        table_html = table.get_attribute('innerHTML')
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(table_html, 'html.parser')
        
        # Find all rows in the table
        rows = soup.find_all('tr')
        
        # List to hold the extracted data
        processors = []
        
        # Iterate through each row and extract data
        for row in rows:
            processor_data = {}
            
            # Extracting data for each row
            processor_name = row.find("div", class_="table_title")
            brand = row.find("div", class_="detail__value f_brand")
            model = row.find("div", class_="detail__value f_model")
            cores = row.find("div", class_="detail__value f_cores")
            threads = row.find("div", class_="detail__value f_threads")
            socket_type = row.find("div", class_="detail__value f_socket_type")
            base_speed = row.find("div", class_="detail__value f_maximum_speed")
            turbo_speed = row.find("div", class_="detail__value f_maximum_speed")
            architecture = row.find("div", class_="detail__value f_micro_architecture")
            memory_type = row.find("div", class_="detail__value f_memory_type")
            price = row.find("td", class_="price")
            amazon_link = row.find("a", class_="btn btn-primary component-btn")
            
            # Only process rows that contain valid data
            if processor_name:
                processor_data["Processor Name"] = processor_name.text.strip()
                processor_data["Brand"] = brand.text.strip() if brand else "N/A"
                processor_data["Model"] = model.text.strip() if model else "N/A"
                processor_data["Cores"] = cores.text.strip() if cores else "N/A"
                processor_data["Threads"] = threads.text.strip() if threads else "N/A"
                processor_data["Socket Type"] = socket_type.text.strip() if socket_type else "N/A"
                processor_data["Base Speed"] = base_speed.text.strip() if base_speed else "N/A"
                processor_data["Turbo Speed"] = turbo_speed.text.strip() if turbo_speed else "N/A"
                processor_data["Architecture"] = architecture.text.strip() if architecture else "N/A"
                processor_data["Memory Type"] = memory_type.text.strip() if memory_type else "N/A"
                processor_data["Price"] = price.text.strip() if price else "N/A"
                processor_data["Amazon Link"] = amazon_link['href'] if amazon_link else "N/A"
                
                # Append the processor data to the list
                processors.append(processor_data)
        
        # Save the data as a JSON file
        with open("processors_data.json", "w", encoding="utf-8") as json_file:
            json.dump(processors, json_file, ensure_ascii=False, indent=4)
        
        print("Data has been saved to processors_data.json")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    get_table_content()
