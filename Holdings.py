import requests
import csv

def get_scheme_data(scheme_code):
    url = f"https://www.rupeevest.com/home/get_mf_portfolio_tracker?schemecode={scheme_code}"
    response = requests.get(url)
    return response.json()

def extract_data(json_data):
    fund_info = json_data.get("fund_info", [])
    stock_data = json_data.get("stock_data", [])

    extracted_data = []
    for fund in fund_info:
        for stock_entry in stock_data:
            for stock in stock_entry:
                entry = {
                    "s_name": fund.get("s_name", ""),
                    "aumdate": fund.get("aumdate", ""),
                    "aumtotal": fund.get("aumtotal", ""),
                    "fincode": stock.get("fincode", ""),
                    "invdate": stock.get("invdate", ""),
                    "noshares": stock.get("noshares", ""),
                    "percent_aum": stock.get("percent_aum", ""),
                }
                extracted_data.append(entry)

    return extracted_data

def main():
    # Read scheme codes from MFCodes.csv
    with open('MFCodes.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        scheme_codes = [row['schemecode'] for row in reader]

    # Fetch data for each scheme code and store in a list
    data_list = []
    for scheme_code in scheme_codes:
        scheme_data = get_scheme_data(scheme_code)
        extracted_data = extract_data(scheme_data)
        data_list.extend(extracted_data)

    # Write the collected data to a CSV file
    with open('MFHoldings.csv', 'w', newline='') as csvfile:
        fieldnames = ["s_name", "aumdate", "aumtotal", "fincode", "invdate", "noshares", "percent_aum"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for entry in data_list:
            writer.writerow(entry)

if __name__ == "__main__":
    main()
