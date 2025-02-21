import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from file_handler import upload_file  # Import the unified upload function
from compare import get_table_names, get_column_names, compare_data  # Import comparison functions

db_sqlite = "sqlite_db"
col_names = None
data = None

# Function to save data to an Excel file
def save_fetchall_to_excel(data, col_names, filename="output.xlsx"):
    if data and col_names:
        df = pd.DataFrame(data, columns=col_names)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Data saved successfully to {file_path}")
    else:
        messagebox.showerror("Error", "No data available to save.")

# Function to trigger saving
def call_save_file():
    global data, col_names
    save_fetchall_to_excel(data, col_names)

# Creating the root window
root = tk.Tk()
root.title("Excel File Comparison and Filtering")
root.geometry("800x600")  # Set initial size of the window

# Label to show the status of file uploads
file_status_label = tk.Label(root, text="No files uploaded yet.", width=50)
file_status_label.pack(pady=10)

# Upload first file
def upload_first_file():
    file_path = upload_file(1)  # Assuming upload_file() returns the file path
    if file_path:
        file_status_label.config(text=f"First file uploaded: {file_path}")
        update_table_comboboxes()  # Update the table comboboxes after file upload
    else:
        messagebox.showerror("Error", "Failed to upload the first file.")

upload_button_1 = tk.Button(root, text="Upload First Excel File", command=upload_first_file)
upload_button_1.pack(pady=10)

# Upload second file
def upload_second_file():
    file_path = upload_file(2)  # Assuming upload_file() returns the file path
    if file_path:
        file_status_label.config(text=f"Second file uploaded: {file_path}")
        update_table_comboboxes()  # Update the table comboboxes after file upload
    else:
        messagebox.showerror("Error", "Failed to upload the second file.")

upload_button_2 = tk.Button(root, text="Upload Second Excel File", command=upload_second_file)
upload_button_2.pack(pady=10)

# Update table comboboxes based on the tables in the SQLite DB
def update_table_comboboxes():
    tables = get_table_names(db_sqlite)
    table_combobox_1['values'] = tables
    table_combobox_2['values'] = tables

# Update column comboboxes based on selected table
def update_column_combobox(table_combobox, column_combobox):
    selected_table = table_combobox.get()
    if selected_table:
        columns = get_column_names(selected_table, db_sqlite)
        column_combobox['values'] = columns

# Function to handle the compare button click event
def compare_button_pressed():
    try:
        global data, col_names
        matched_data = compare_data(db_sqlite, table_combobox_1, table_combobox_2, column_combobox_1, column_combobox_2, value_entry)
        data = matched_data

        # Store column names
        table_1 = table_combobox_1.get()
        table_2 = table_combobox_2.get()
        columns_1 = get_column_names(table_1, db_sqlite)
        columns_2 = get_column_names(table_2, db_sqlite)
        col_names = [f"{column}-table1" for column in columns_1] + [f"{column}-table2" for column in columns_2]

        display_matched_data_in_treeview(matched_data)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during comparison: {e}")

# Function to display matched data in the Treeview widget
def display_matched_data_in_treeview(matched_data):
    # Clear previous data in the Treeview
    for row in result_treeview.get_children():
        result_treeview.delete(row)

    if matched_data:
        # Set Treeview columns
        result_treeview["columns"] = col_names
        for col in col_names:
            result_treeview.heading(col, text=col)
            result_treeview.column(col, width=150, anchor="center")

        # Insert rows into the Treeview
        for row in matched_data:
            result_treeview.insert("", "end", values=row)
    else:
        messagebox.showinfo("No Matches", "No matching data found between the tables.")

# Compare Button
compare_button = tk.Button(root, text="Compare Data", command=compare_button_pressed)
compare_button.pack(pady=10)

# Save Data Button (Fixed function call)
save_button = tk.Button(root, text="Save Data", command=call_save_file)
save_button.pack(pady=10)

# Table selection comboboxes
table_combobox_1 = ttk.Combobox(root)
table_combobox_1.pack(pady=5)
table_combobox_1.bind("<<ComboboxSelected>>", lambda event: update_column_combobox(table_combobox_1, column_combobox_1))

table_combobox_2 = ttk.Combobox(root)
table_combobox_2.pack(pady=5)
table_combobox_2.bind("<<ComboboxSelected>>", lambda event: update_column_combobox(table_combobox_2, column_combobox_2))

# Column selection comboboxes
column_combobox_1 = ttk.Combobox(root)
column_combobox_1.pack(pady=5)

column_combobox_2 = ttk.Combobox(root)
column_combobox_2.pack(pady=5)

# Value entry box (for specific value filter)
value_entry = tk.Entry(root)
value_entry.pack(pady=5)

# Frame to contain the Treeview and scrollbars
frame = tk.Frame(root)
frame.pack(pady=10, fill="both", expand=True)

# Create the Treeview widget with scrollbars inside
result_treeview = ttk.Treeview(frame, show="headings")

# Create vertical scrollbar for Treeview
vertical_scrollbar = tk.Scrollbar(frame, orient="vertical", command=result_treeview.yview)
result_treeview.configure(yscrollcommand=vertical_scrollbar.set)

# Create horizontal scrollbar for Treeview
horizontal_scrollbar = tk.Scrollbar(frame, orient="horizontal", command=result_treeview.xview)
result_treeview.configure(xscrollcommand=horizontal_scrollbar.set)

# Use grid layout for proper alignment
result_treeview.grid(row=0, column=0, sticky="nsew")
vertical_scrollbar.grid(row=0, column=1, sticky="ns")
horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

# Configure the frame to expand properly
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Fetch table names and update comboboxes after file upload
update_table_comboboxes()

# Handle window close event
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()  # Close the window and terminate the program

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()
