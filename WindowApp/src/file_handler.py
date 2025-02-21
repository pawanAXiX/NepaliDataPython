import tkinter as tk
import pandas as pd
from tkinter import filedialog, messagebox
from tkinter import ttk

# Global variables for storing the data frames and sheet names
df_1 = None
df_2 = None
name_1 = ""
name_2 = ""


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
                return filepath

            # If the file contains only one sheet
            else:
                df = pd.read_excel(filepath)
                if file_num == 1:
                    df_1 = df
                    name_1 = excel_data.sheet_names[0]
                elif file_num == 2:
                    df_2 = df
                    name_2 = excel_data.sheet_names[0]
                messagebox.showinfo("Success", f"Sheet '{name_1 if file_num == 1 else name_2}' successfully loaded!")
                return filepath

        except Exception as e:
            # Handle errors, such as non-Excel files or incorrect file formats
            messagebox.showerror("Error", f"Error reading file: {e}")
    else:
        messagebox.showerror("Error", "No file selected")

