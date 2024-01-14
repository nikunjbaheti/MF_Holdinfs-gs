import requests
import csv
import json

def fetch_data_and_save_csv(script_code_url, api_url, csv_filename):
    # Fetch script codes from the CSV
    script_code_response = requests.get(script_code_url)
    
    if script_code_response.status_code == 200:
        # Extract script codes from the CSV
        script_code_data = csv.DictReader(script_code_response.text.splitlines())
        script_codes = [row['SCRIP_CD'] for row in script_code_data]

        # Fetch data for each script code
        for script_code in script_codes:
            full_api_url = f"{api_url}{script_code}"
            response = requests.get(full_api_url)

            if response.status_code == 200:
                data = response.json()

                # Extract relevant information from the JSON response
                header = data.get('Header', {})
                records = data.get('Data', [])

                # Prepare CSV data
                csv_data = []
                csv_header = [
                    "Security Id", "Group Index", "Face Value", "Security Code", "ISIN", "Industry",
                    "Group", "Index", "Paid-up Value", "EPS", "CEPS", "PE", "OPM", "NPM", "PB", "ROE",
                    "Sector", "Industry New", "Industry Group", "Industry Sub-Group", "IShow", "Settlement Type",
                    "Company Name", "Contact", "Email", "SDD", "Company Details", "SDD Scrip"
                ]

                for record in records:
                    csv_row = [
                        record.get("SecurityId"), record.get("Grp_Index"), record.get("FaceVal"),
                        record.get("SecurityCode"), record.get("ISIN"), record.get("Industry"),
                        record.get("Group"), record.get("Index"), record.get("PAIDUP_VALUE"),
                        record.get("EPS"), record.get("CEPS"), record.get("PE"), record.get("OPM"),
                        record.get("NPM"), record.get("PB"), record.get("ROE"), record.get("Sector"),
                        record.get("IndustryNew"), record.get("IGroup"), record.get("ISubGroup"),
                        record.get("IShow"), record.get("SetlType"), record.get("COName"),
                        record.get("Contact"), record.get("Email"), record.get("SDD"),
                        record.get("COdetails"), record.get("sddscrip")
                    ]
                    csv_data.append(csv_row)

                # Write data to CSV file
                output_filename = f"{script_code}_{csv_filename}"
                with open(output_filename, 'w', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    
                    # Write header
                    csv_writer.writerow(csv_header)
                    
                    # Write data rows
                    csv_writer.writerows(csv_data)

                print(f"CSV file '{output_filename}' has been created successfully.")
            else:
                print(f"Failed to fetch data for script code {script_code}. Status code: {response.status_code}")
    else:
        print(f"Failed to fetch script codes from CSV. Status code: {script_code_response.status_code}")

if __name__ == "__main__":
    # URL of the script codes CSV
    script_code_url = "https://raw.githubusercontent.com/nikunjbaheti/MF_Holdings/main/BSEData.csv"

    # Base URL of the API
    api_url = "https://api.bseindia.com/BseIndiaAPI/api/ComHeadernew/w?quotetype=EQ&scripcode="

    # CSV filename
    csv_filename = "BSE_StkData.csv"

    # Fetch data and save to CSV
    fetch_data_and_save_csv(script_code_url, api_url, csv_filename)
