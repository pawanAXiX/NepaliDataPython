
from tkinter import filedialog, messagebox

import sqlite3
import pandas as pd
import os

# Global variables for storing the data frames and sheet names
df_1 = None
df_2 = None
name_1 = ""
name_2 = ""
db_sqlite='sqlite_db'


# Function to delete the existing SQLite database and create a new one
def create_new_db(db_file):
    # Delete the existing database file if it exists
    # Create a new database connection (this will create a new empty database)
    conn = sqlite3.connect(db_file)
    return conn



def upload_file(file_num):
    filepath = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])

    # If a file is selected
    if filepath:
        try:
            global df_1, df_2, name_1, name_2
            excel_data = pd.ExcelFile(filepath)

            # If the file contains two or more sheets
            if len(excel_data.sheet_names) >= 2:
                df_1 = pd.read_excel(filepath, sheet_name=excel_data.sheet_names[0])  # First sheet
                df_2 = pd.read_excel(filepath, sheet_name=excel_data.sheet_names[1])  # Second sheet
                name_1 = excel_data.sheet_names[0]
                name_2 = excel_data.sheet_names[1]
                messagebox.showinfo("Success", "Both sheets have been successfully loaded!")
                insert_data_from_excel_to_db(df_1,name_1,db_sqlite)
                insert_data_from_excel_to_db(df_2, name_2, db_sqlite)
                return filepath

            # If the file contains only one sheet
            else:
                df = pd.read_excel(filepath)
                if file_num == 1:
                    df_1 = df
                    name_1 = excel_data.sheet_names[0]
                    insert_data_from_excel_to_db(df_1, name_1, db_sqlite)
                elif file_num == 2:
                    df_2 = df
                    name_2 = excel_data.sheet_names[0]
                    insert_data_from_excel_to_db(df_2, name_2, db_sqlite)
                messagebox.showinfo("Success", f"Sheet '{name_1 if file_num == 1 else name_2}' successfully loaded!")
                return filepath

        except Exception as e:
            # Handle errors, such as non-Excel files or incorrect file formats
            messagebox.showerror("Error", f"Error reading file: {e}")
    else:
        messagebox.showerror("Error", "No file selected")


# Function to create table and insert data from Excel into SQLite
def insert_data_from_excel_to_db(df, table_name, db_file):
    # Read the Excel file into a DataFrame with UTF-8 encoding


    # Connect to SQLite database (it will create the file if it doesn't exist)
    conn = create_new_db(db_file)
    cursor = conn.cursor()

    columns = []
    for col in df.columns:
        # Assuming text type for string columns and integer for numeric ones
        col_type = 'TEXT' if df[col].dtype == 'object' else 'INTEGER'
        columns.append(f"`{col}` {col_type}")  # Use backticks to allow non-English characters

    # Create the table with dynamic column names and types
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join(columns)})"
    cursor.execute(create_table_query)

    # Insert data into the table
    for index, row in df.iterrows():
        placeholders = ', '.join(['?'] * len(df.columns))  # Create placeholders for each column
        insert_query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in df.columns])}) VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(row))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Data inserted successfully!")



