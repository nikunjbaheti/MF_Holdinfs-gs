import requests
import csv

url = "https://www.rupeevest.com/stock_price_difference/get_compare_data_stock"
csv_file_name = "Stkcode.csv"

# Make a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    json_data = response.json()

    # Extract relevant data from the JSON response
    data_to_write = []
    for item in json_data.get('stock_compare_data', []):
        fincode = item.get('fincode', '')
        rv_sect_name = item.get('rv_sect_name', '')
        compname = item.get('compname', '')
        classification = item.get('classification', '')

        # Append the data to the list
        data_to_write.append({
            "fincode": fincode,
            "rv_sect_name": rv_sect_name,
            "compname": compname,
            "classification": classification
        })

    # Write the data to a CSV file
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["fincode", "rv_sect_name", "compname", "classification"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data
        for row in data_to_write:
            writer.writerow(row)

    print(f"Data has been successfully written to {csv_file_name}")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
