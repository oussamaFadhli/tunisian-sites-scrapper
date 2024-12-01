import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize an empty list to hold the CPU data
all_cpu_data = []

# Loop through each year from 2020 to 2025
for year in range(2020, 2026):
    # Define the URL with the current year
    url = f"https://www.techpowerup.com/cpu-specs/?released={year}&mobile=No&sort=name"

    # Send a GET request to fetch the HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the CPU data
    table = soup.find('table', {'class': 'processors'})

    # Skip to next iteration if table is not found (e.g., for years without data)
    if not table:
        print(f"No data found for {year}")
        continue

    # Loop through each row in the table (skipping the header rows)
    for row in table.find_all('tr')[2:]:
        columns = row.find_all('td')
        
        if len(columns) > 0:
            cpu_name = columns[0].text.strip()
            codename = columns[1].text.strip()
            cores = columns[2].text.strip()
            clock = columns[3].text.strip()
            socket = columns[4].text.strip()
            process = columns[5].text.strip()
            cache = columns[6].text.strip()
            tdp = columns[7].text.strip()
            released = columns[8].text.strip()

            # Append the data to the list
            all_cpu_data.append({
                'Name': cpu_name,
                'Codename': codename,
                'Cores': cores,
                'Clock': clock,
                'Socket': socket,
                'Process': process,
                'L3 Cache': cache,
                'TDP': tdp,
                'Released': released
            })

# Convert the list of dictionaries into a DataFrame for easy manipulation
df = pd.DataFrame(all_cpu_data)



# Optionally, save the data to a CSV file
df.to_csv('cpu_specs_2020_2025.csv', index=False)
