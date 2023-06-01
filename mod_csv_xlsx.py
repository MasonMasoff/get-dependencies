# Converts CSV file to XLSX
import pandas as pd
import variables

def convert_csv_to_xlsx(csv_file, xlsx_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Write the DataFrame to an XLSX file
    df.to_excel(xlsx_file, index=False)

# Specify the file paths
csv_file_path = variables.csv_file_path
xlsx_file_path = variables.xlsx_file_path

# Convert the CSV file to XLSX
convert_csv_to_xlsx(csv_file_path, xlsx_file_path)

print("CSV successfully converted.")
