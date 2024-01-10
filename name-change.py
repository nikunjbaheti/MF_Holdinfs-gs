import pandas as pd
import requests
from io import StringIO

# URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/nikunjbaheti/MF_Holdings/main/StkCode.csv'

# Fetch the CSV file from the URL
response = requests.get(csv_url)
csv_data = response.text

# Read the CSV data using pandas
df = pd.read_csv(StringIO(csv_data), delimiter='\t')

# Function to replace "Ltd" and "Ltd." with "Limited" and convert to proper case
def clean_and_proper_case(row):
    return row.str.replace('Ltd.', 'Limited', case=False).str.replace('Ltd', 'Limited', case=False).str.title()

# Remove "EQ - " from all columns
df = df.apply(lambda col: col.str.replace('EQ - ', '', case=False))

# Apply the replacement function and proper case conversion to all columns
df = df.apply(clean_and_proper_case)

# Write the modified data back to a new CSV file
output_file_path = 'modified_StkCode.csv'
df.to_csv(output_file_path, sep='\t', index=False)

print(f"Modification complete. Data written to {output_file_path}")
