import requests
import csv

url = "https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w?Group=&Scripcode=&industry=&segment=Equity&status=Active"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses

    data = response.json()

    # Extracting relevant data
    extracted_data = []
    for item in data:
        entry = {
            "SCRIP_CD": item["SCRIP_CD"],
            "scrip_id": item["scrip_id"],
            "Scrip_Name": item["Scrip_Name"],
            "Issuer_Name": item["Issuer_Name"],
        }
        extracted_data.append(entry)

    # Saving to CSV
    with open("BSEData.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["SCRIP_CD", "scrip_id", "Scrip_Name", "Issuer_Name"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        writer.writerows(extracted_data)

    print("Data has been saved to BSEData.csv")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
