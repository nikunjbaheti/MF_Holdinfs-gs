import requests
import time
from bs4 import BeautifulSoup
import csv

# Navigate to the list of scrips page
website_url = "https://mock.bseindia.com/corporates/List_Scrips.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.bseindia.com/",
}

try:
    website_response = requests.get(website_url, headers=headers)
    website_response.raise_for_status()

    # Assuming the website contains the necessary information to make the API request,
    # extract any required data or cookies from the website's HTML.

    # Example: Extracting cookies
    cookies = website_response.cookies

    # Wait for 30 seconds
    time.sleep(30)

    # Now, make the API request
    api_url = "https://mockapi.bseindia.com/BseIndiaAPI/api/ListofScripData/w?Group=&Scripcode=&industry=&segment=Equity&status=Active"
    api_headers = {
        "User-Agent": headers["User-Agent"],
        "Accept-Language": headers["Accept-Language"],
        "Accept-Encoding": headers["Accept-Encoding"],
        "Referer": headers["Referer"],
        # Add any other necessary headers here
    }

    api_response = requests.get(api_url, headers=api_headers, cookies=cookies)
    api_response.raise_for_status()

    try:
        api_data = api_response.json()

        # Extracting relevant data
        extracted_data = []
        for item in api_data:
            entry = {
                "SCRIP_CD": item.get("SCRIP_CD"),
                "scrip_id": item.get("scrip_id"),
                "Scrip_Name": item.get("Scrip_Name"),
                "Issuer_Name": item.get("Issuer_Name"),
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

    except ValueError:
        print("Error: Invalid JSON format in API response")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
