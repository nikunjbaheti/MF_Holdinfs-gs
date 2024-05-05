import requests
import csv

def fetch_json_and_save_csv():
    # Read dynamic numbers and MFCode from MFCodes.csv starting from the second row
    with open('MFCodes.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        mf_data = [(row[2], row[2]) for row in reader]  # MFCode is in the first column

    # Specify the CSV file name for output
    output_csv_filename = 'Benchmarks.csv'

    for mf_code, dynamic_number in mf_data:
        # Construct the URL with the dynamic number
        url = f'https://www.rupeevest.com/home/get_indexe_name_scheme_wise?schemecode={dynamic_number}'

        try:
            # Fetch JSON data from the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Parse JSON data
            json_data = response.json()['index_name']

            # Write JSON data to CSV file
            with open(output_csv_filename, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)

                # Write header if the file is empty
                if csvfile.tell() == 0:
                    csvwriter.writerow(['MFCode', 'indexcode', 'indexname', 'weightage'])

                # Write data rows
                for item in json_data:
                    csvwriter.writerow([mf_code, item['indexcode'], item['indexname'], item['weightage']])

            print(f'Data for MFCode={mf_code} and schemecode={dynamic_number} successfully fetched and appended to {output_csv_filename}')

        except requests.exceptions.RequestException as e:
            print(f'Error fetching data from {url}: {e}')

if __name__ == "__main__":
    fetch_json_and_save_csv()
