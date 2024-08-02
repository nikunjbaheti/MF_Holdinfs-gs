import requests
import csv

def fetch_json_and_save_csv():
    input_csv_filename = 'MFCodes.csv'
    output_csv_filename = 'Index_Latest.csv'

    with open(input_csv_filename, 'r') as input_csvfile:
        reader = csv.reader(input_csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            mf_code = row[0]  # Assuming MF Code is in the first column
            dynamic_number = row[2]  # Assuming dynamic number is in the third column

            # Construct the URL with the dynamic number
            url = f'https://www.rupeevest.com/home/index_latest_new?schemecode={dynamic_number}'

            try:
                # Fetch JSON data from the URL
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad responses

                # Parse JSON data
                json_data = response.json().get('schemedata', [])

                # If json_data is empty, skip to the next iteration
                if not json_data:
                    print(f"No data returned for schemecode {dynamic_number}")
                    continue

                # Write JSON data to CSV file
                with open(output_csv_filename, 'a', newline='') as output_csvfile:
                    csvwriter = csv.writer(output_csvfile)

                    # Write header if the file is empty
                    if output_csvfile.tell() == 0:
                        csvwriter.writerow(['MF Code'] + list(json_data[0].keys()))  # Include MF Code in the header

                    # Write data rows
                    for item in json_data:
                        csvwriter.writerow([mf_code] + list(item.values()))  # Append MF Code to each row

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for MFCode {mf_code}: {e}")

if __name__ == "__main__":
    fetch_json_and_save_csv()
