import requests
import csv

def fetch_json_and_save_csv():
    # Specify the CSV file name for output
    output_csv_filename = 'Historical_returns.csv'

    with open('MFCodes.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            # Extract dynamic number from the current row
            dynamic_number = row[2]  # Assuming dynamic number is in the third column

            # Construct the URL with the dynamic number
            url = f'https://www.rupeevest.com/functionalities/get_returns_year?schemecode={dynamic_number}'

            try:
                # Fetch JSON data from the URL
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for bad responses

                # Parse JSON data
                json_data = response.json().get('returns_year', [])

                # If json_data is empty, skip to the next iteration
                if not json_data:
                    print(f"No data returned for schemecode {dynamic_number}")
                    continue

                # Write JSON data to CSV file
                with open(output_csv_filename, 'a', newline='') as output_csvfile:
                    csvwriter = csv.writer(output_csvfile)

                    # Write header if the file is empty
                    if output_csvfile.tell() == 0:
                        csvwriter.writerow(json_data[0].keys())

                    # Write data rows
                    for item in json_data:
                        csvwriter.writerow(item.values())

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data for schemecode {dynamic_number}: {e}")

if __name__ == "__main__":
    fetch_json_and_save_csv()
