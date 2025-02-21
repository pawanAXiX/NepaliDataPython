


import tkinter as tk
import pandas as pd
from tkinter import filedialog, messagebox, simpledialog
import file_handler
from tkinter import ttk

import os

check=False
def display(common_matching_rows):
    # Ask the user for the path to save the Excel file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")],
                                             title="Save Matching Rows")

    if file_path:
        try:
            # Save the DataFrame to an Excel file
            common_matching_rows.to_excel(file_path, index=False)
            messagebox.showinfo("File Saved", f"Matching data has been saved to {file_path}")
            global check
            check=True
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


