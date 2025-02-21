# import tkinter as tk
# from tkinter import filedialog, messagebox
# from tkinter import ttk
# import sqlite3
# import pandas as pd
# import os
# from compare import get_table_names, get_column_names, compare_data  # Import the functions
#
# # Global variables for storing the data frames and sheet names
# df_1 = None
# df_2 = None
# name_1 = ""
# name_2 = ""
# db_sqlite = 'sqlite_db'
#
# def update_table_comboboxes():
#     tables = get_table_names(db_sqlite)
#     table_combobox_1['values'] = tables
#     table_combobox_2['values'] = tables
#
# # Function to handle the compare button click event
# def compare_button_pressed():
#     try:
#         compare_data(db_sqlite, table_combobox_1, table_combobox_2, column_combobox_1, column_combobox_2, value_entry)
#     except Exception as e:
#         messagebox.showerror("Error", f"An error occurred during comparison: {e}")
#
# # Creating the root window
# root = tk.Tk()
# root.title("Excel File Comparison and Filtering")
# root.geometry("800x600")
#
# # Upload first file button
# upload_button_1 = tk.Button(root, text="Upload First Excel File", command=lambda: upload_file(1))
# upload_button_1.pack(pady=10)
#
# # Upload second file button
# upload_button_2 = tk.Button(root, text="Upload Second Excel File", command=lambda: upload_file(2))
# upload_button_2.pack(pady=10)
#
# # Compare Button
# compare_button = tk.Button(root, text="Compare Data", command=compare_button_pressed)
# compare_button.pack(pady=10)
#
# # Table selection comboboxes
# table_combobox_1 = ttk.Combobox(root)
# table_combobox_1.pack(pady=10)
#
# table_combobox_2 = ttk.Combobox(root)
# table_combobox_2.pack(pady=10)
#
# # Column selection comboboxes
# column_combobox_1 = ttk.Combobox(root)
# column_combobox_1.pack(pady=10)
#
# column_combobox_2 = ttk.Combobox(root)
# column_combobox_2.pack(pady=10)
#
# # Value entry box
# value_entry = tk.Entry(root)
# value_entry.pack(pady=10)
#
# # Fetch table names and update comboboxes after file upload
# update_table_comboboxes()
#
# # Start the Tkinter main loop
# root.mainloop()
