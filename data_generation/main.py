import pandas as pd
from utility import *
from jproperties import Properties
import logging
import csv

# ---------------- Load Properties ---------------- #
configs = Properties()
with open('app-config.properties', 'rb') as config_file:
    configs.load(config_file)

filename = configs.get("filename").data
sheet = configs.get("sheet").data
json_file_name = configs.get("json_file_name").data
log_file_name = configs.get("log_file_name").data

# ---------------- Helper ---------------- #
def number_of_records_to_generate():
    try:
        total_count = int(input("How many records do you need?\n Number : "))
        return total_count
    except Exception as e:
        print("Invalid input. Defaulting to 10 records.")
        return 10

# ---------------- Excel to DataFrame ---------------- #
def read_excel_to_dataframe(filename, sheet):
    try:
        df = pd.read_excel(filename, sheet_name=sheet)
        df = df.where(pd.notnull(df), None)  # Convert all NaN to None
        return df
    except Exception as e:
        logger.error(f"Error reading Excel file {filename}: {str(e)}")
        return None

# ---------------- Data Generation ---------------- #
def generate_data(df, total_count):
    try:
        output = {}
        for _, row in df.iterrows():
            field_name = row.get("Field")
            output[field_name] = generate_field(row, total_count)
        return output
    except Exception as e:
        logger.error(f"Error in generate_data: {str(e)}")
        return None

# ---------------- Write CSV ---------------- #
def write_csv(data, filename):
    try:
        fields = list(data.keys())
        total_count = len(data[fields[0]])
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            for i in range(total_count):
                writer.writerow([data[field][i] for field in fields])
        logger.info(f"CSV file generated successfully: {filename}")
        print(f"CSV file generated successfully: {filename}")
    except Exception as e:
        logger.error(f"Error writing CSV file: {str(e)}")

# ---------------- Main Execution ---------------- #
def initiate_data_generation():
    try:
        print("START : [initiate_data_generation] : Start of method execution.")
        total_count = number_of_records_to_generate()

        df = read_excel_to_dataframe(filename, sheet)
        if df is None:
            print("Failed to read input Excel. Exiting.")
            return

        data = generate_data(df, total_count)
        if data is None:
            print("Data generation failed. Exiting.")
            return

        output_csv = filename.split(".")[0] + "_generated.csv"
        write_csv(data, output_csv)

        print("END : [initiate_data_generation] : DATA GENERATED SUCCESSFULLY.")
        logger.info("--------------------------------------------------------------------------------------------------------------")
    except Exception as e:
        print(f"ERROR : [initiate_data_generation] : DATA GENERATION FAILED : {str(e)}")
        logger.error(f"DATA GENERATION FAILED: {str(e)}")

# ---------------- Run ---------------- #
if __name__ == "__main__":
    initiate_data_generation()
