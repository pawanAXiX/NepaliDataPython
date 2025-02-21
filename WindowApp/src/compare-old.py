import tkinter as tk
import pandas as pd
from tkinter import filedialog, messagebox, simpledialog
import file_handler
from display import display
from tkinter import ttk

def select_column_from_table(table_df, title="Select Columns"):
    column_select_window = tk.Toplevel()
    column_select_window.title(title)
    column_select_window.geometry("400x300")
    column_select_window.lift()  # Bring the window on top

    listbox = tk.Listbox(column_select_window, selectmode=tk.MULTIPLE)

    for col in table_df.columns:
        listbox.insert(tk.END, col)
    listbox.pack(padx=10, pady=10)

    selected_columns = []

    def confirm_selection():
        nonlocal selected_columns
        selected_columns = [listbox.get(i) for i in listbox.curselection()]
        if selected_columns:
            column_select_window.destroy()
        else:
            messagebox.showerror("Error", "No columns selected")

    confirm_button = tk.Button(column_select_window, text="Confirm Selection", command=confirm_selection)
    confirm_button.pack(pady=5)
    column_select_window.wait_window()
    return selected_columns

#
# def compare_data():
#     def start_comparison():
#         table_choice = simpledialog.askstring("Input",
#                                               "Select the number of tables to compare with (1 for comparing within a single table/sheet, 2 for comparing with another table):")
#         if table_choice not in ['1', '2']:
#             messagebox.showerror("Error", "Please select either 1 or 2:")
#             return
#
#         def update_progress(message):
#             status_label.config(text=message)
#             progress_window.update_idletasks()
#
#         if table_choice == '1':
#             table_1_choice = simpledialog.askstring("Input",
#                                                     f"Enter the name of table (Available sheets: {file_handler.name_1}, {file_handler.name_2}):").strip()
#             if table_1_choice == file_handler.name_1:
#                 df_1_selected = file_handler.df_1
#             elif table_1_choice == file_handler.name_2:
#                 df_1_selected = file_handler.df_2
#             else:
#                 messagebox.showerror("Error", "Invalid Table Name")
#                 return
#
#             selected_columns = select_column_from_table(df_1_selected, f"Select Columns from {table_1_choice}")
#             if not selected_columns:
#                 messagebox.showerror("Error", "No columns selected")
#                 return
#
#             compare_value = simpledialog.askstring("Input",
#                                                    f"Enter the value to compare in columns {selected_columns} (Leave empty to compare all values):")
#
#             update_progress("Processing data...")  # Set initial processing message
#
#             matching_rows = df_1_selected
#             if compare_value:
#                 matching_rows = df_1_selected[df_1_selected[selected_columns[0]] == compare_value]
#                 for col in selected_columns[1:]:
#                     matching_rows = matching_rows[matching_rows[col] == compare_value]
#
#             # Merge all matching rows into a single row
#             merged_matching_rows = matching_rows
#
#             # Process rows one by one to simulate row-by-row checking
#             total_rows = len(merged_matching_rows)
#             checked_rows = 0
#
#             def process_next_row():
#                 nonlocal checked_rows
#                 if checked_rows < total_rows:
#                     checked_row = merged_matching_rows.iloc[checked_rows]
#                     # Simulate comparison logic here
#                     checked_rows += 1
#                     update_progress(f"Processing row {checked_rows}/{total_rows}...")
#                     progress_window.after(10, process_next_row)  # Process next row after a short delay
#                 else:
#                     update_progress("Done!")
#                     progress_window.after(2000, progress_window.destroy)  # Close progress window after 2 seconds
#
#                     # After processing all rows, display the results
#                     display(merged_matching_rows)  # Show the results or save to an Excel file
#
#             process_next_row()  # Start processing rows
#
#         elif table_choice == '2':
#             table_1_choice = simpledialog.askstring("Input",
#                                                     f"Enter the name of Table 1 (Available sheets: {file_handler.name_1}, {file_handler.name_2}):").strip()
#             table_2_choice = simpledialog.askstring("Input",
#                                                     f"Enter the name of Table 2 (Available sheets: {file_handler.name_1}, {file_handler.name_2}):").strip()
#
#             if table_1_choice == file_handler.name_1:
#                 df_1_selected = file_handler.df_1
#             elif table_1_choice == file_handler.name_2:
#                 df_1_selected = file_handler.df_2
#             else:
#                 messagebox.showerror("Error", "Invalid Table 1 name.")
#                 return
#
#             if table_2_choice == file_handler.name_1:
#                 df_2_selected = file_handler.df_1
#             elif table_2_choice == file_handler.name_2:
#                 df_2_selected = file_handler.df_2
#             else:
#                 messagebox.showerror("Error", "Invalid Table 2 name.")
#                 return
#
#             selected_columns_1 = select_column_from_table(df_1_selected, f"Select Columns from {table_1_choice}")
#             selected_columns_2 = select_column_from_table(df_2_selected, f"Select Columns from {table_2_choice}")
#
#             if not selected_columns_1 or not selected_columns_2:
#                 messagebox.showerror("Error", "No columns selected in one of the tables.")
#                 return
#
#             if len(selected_columns_1) != len(selected_columns_2):
#                 messagebox.showerror("Error", "Please select the same number of columns from both tables.")
#                 return
#
#             compare_value = simpledialog.askstring("Input",
#                                                    f"Enter the value to compare in columns {selected_columns_1} (Leave empty to compare all values):")
#
#             update_progress("Processing data...")  # Set initial processing message
#
#             # Process rows one by one to simulate row-by-row checking for both tables
#             total_rows_1 = len(df_1_selected)
#             total_rows_2 = len(df_2_selected)
#             checked_rows_1 = 0
#             checked_rows_2 = 0
#
#             # Empty list to store the merged matching rows
#             merged_matching_rows = []
#
#             def process_next_row():
#                 nonlocal checked_rows_1, checked_rows_2
#                 if checked_rows_1 < total_rows_1 or checked_rows_2 < total_rows_2:
#                     if checked_rows_1 < total_rows_1:
#                         df_1_row = df_1_selected.iloc[checked_rows_1]
#                         checked_rows_1 += 1
#                     if checked_rows_2 < total_rows_2:
#                         df_2_row = df_2_selected.iloc[checked_rows_2]
#                         checked_rows_2 += 1
#
#                     # Merge rows when they match
#                     if compare_value:
#                         if df_1_row[selected_columns_1[0]] == compare_value and df_2_row[
#                             selected_columns_2[0]] == compare_value:
#                             merged_row = pd.concat([df_1_row, df_2_row], axis=0)
#                             merged_matching_rows.append(merged_row)
#                     else:
#                         merged_row = pd.concat([df_1_row, df_2_row], axis=0)
#                         merged_matching_rows.append(merged_row)
#
#                     update_progress(
#                         f"Processing rows {checked_rows_1}/{total_rows_1} (Table 1), {checked_rows_2}/{total_rows_2} (Table 2)...")
#                     progress_window.after(10, process_next_row)  # Process next row after a short delay
#                 else:
#                     update_progress("Done!")
#                     progress_window.after(2000, progress_window.destroy)  # Close progress window after 2 seconds
#
#                     # After processing all rows, convert the list of matching rows to a DataFrame
#                     # Reset index to avoid duplicate index issue
#                     merged_matching_rows_df = pd.DataFrame(merged_matching_rows).reset_index(drop=True)
#
#                     if merged_matching_rows_df.empty:
#                         messagebox.showinfo("No Match Found", "No matching rows found based on your criteria.")
#                     else:
#                         print(f"Found {len(merged_matching_rows_df)} matching rows.")
#                         # Call the display function to show or save the results
#                         display(merged_matching_rows_df)
#
#             process_next_row()  # Start processing rows
#
#     # Show the progress window
#     progress_window = tk.Toplevel()
#     progress_window.title("Processing")
#     progress_window.geometry("300x100")
#
#     status_label = tk.Label(progress_window, text="Waiting for input...", width=40)
#     status_label.pack(pady=20)
#
#     # Use after to allow the Tkinter event loop to handle user input
#     progress_window.after(10, start_comparison)  # Start comparison after 10 ms to prevent blocking the UI


import unicodedata


# Utility to update the progress
def update_progress(progress_label, message):
    progress_label.config(text=message)
    progress_label.update_idletasks()

# Utility to handle matching data for a single table
def process_single_table(df_selected, selected_columns, compare_value, progress_label):
    # Filter data based on the comparison value if provided
    if compare_value:
        matching_rows = df_selected[df_selected[selected_columns[0]] == compare_value]
        for col in selected_columns[1:]:
            matching_rows = matching_rows[matching_rows[col] == compare_value]
    else:
        matching_rows = df_selected

    return matching_rows


# Utility to handle comparison between two tables
def process_multiple_tables(df_1, df_2, selected_columns_1, selected_columns_2, compare_value, progress_label):
    # Process rows one by one for table 1 and table 2
    total_rows_1 = len(df_1)
    total_rows_2 = len(df_2)
    checked_rows_1 = 0
    checked_rows_2 = 0
    common_matching_rows = []

    while checked_rows_1 < total_rows_1 or checked_rows_2 < total_rows_2:
        if checked_rows_1 < total_rows_1:
            df_1_row = df_1.iloc[checked_rows_1]
            checked_rows_1 += 1
        if checked_rows_2 < total_rows_2:
            df_2_row = df_2.iloc[checked_rows_2]
            checked_rows_2 += 1

        # Merge or compare rows (simple check for match in selected columns)
        if all(df_1_row[col_1] == df_2_row[col_2] for col_1, col_2 in zip(selected_columns_1, selected_columns_2)):
            common_matching_rows.append(df_1_row)

        update_progress(progress_label, f"Processing rows: {checked_rows_1}/{total_rows_1} (Table 1), {checked_rows_2}/{total_rows_2} (Table 2)")

    return pd.DataFrame(common_matching_rows)

# Function to display the matching rows and allow the user to save them
def display_and_save(common_matching_rows):
    if common_matching_rows.empty:
        messagebox.showinfo("No Matches", "No matching rows found based on your criteria.")
        return

    # Ask the user for the path to save the Excel file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")],
                                             title="Save Matching Rows")
    if file_path:
        try:
            # Save the DataFrame to an Excel file
            common_matching_rows.to_excel(file_path, index=False)
            messagebox.showinfo("File Saved", f"Matching data has been saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


# Main comparison function
def compare_data():
    def start_comparison():
        table_choice = simpledialog.askstring("Input",
                                              "Select the number of tables to compare with (1 for comparing within single table/sheet, 2 for comparing with other table):")
        if table_choice not in ['1', '2']:
            messagebox.showerror("Error", "Please select either 1 or 2:")
            return

        def handle_single_table_comparison(df_1_selected, progress_label):
            table_1_choice = simpledialog.askstring("Input",
                                                    f"Enter the name of table (Available sheets: {file_handler.name_1}, {file_handler.name_2}):").strip()
            if table_1_choice == file_handler.name_1:
                df_selected = file_handler.df_1
            elif table_1_choice == file_handler.name_2:
                df_selected = file_handler.df_2
            else:
                messagebox.showerror("Error", "Invalid Table Name")
                return

            selected_columns = select_column_from_table(df_selected, f"Select Columns from {table_1_choice}")
            if not selected_columns:
                messagebox.showerror("Error", "No columns selected")
                return

            compare_value = simpledialog.askstring("Input",
                                                   f"Enter the value to compare in columns {selected_columns} (Leave empty to compare all values):")

            matching_rows = process_single_table(df_selected, selected_columns, compare_value, progress_label)

            display_and_save(matching_rows)  # Display or save the results

        def handle_multiple_table_comparison(df_1_selected, df_2_selected, progress_label):
            table_1_choice = simpledialog.askstring("Input",
                                                    f"Enter the name of Table 1 (Available sheets: {file_handler.name_1}, {file_handler.name_2}):").strip()
            table_2_choice = simpledialog.askstring("Input",
                                                    f"Enter the name of Table 2 (Available sheets: {file_handler.name_1}, {file_handler.name_2}):").strip()

            if table_1_choice == file_handler.name_1:
                df_1_selected = file_handler.df_1
            elif table_1_choice == file_handler.name_2:
                df_1_selected = file_handler.df_2
            else:
                messagebox.showerror("Error", "Invalid Table 1 name.")
                return

            if table_2_choice == file_handler.name_1:
                df_2_selected = file_handler.df_1
            elif table_2_choice == file_handler.name_2:
                df_2_selected = file_handler.df_2
            else:
                messagebox.showerror("Error", "Invalid Table 2 name.")
                return

            selected_columns_1 = select_column_from_table(df_1_selected, f"Select Columns from {table_1_choice}")
            selected_columns_2 = select_column_from_table(df_2_selected, f"Select Columns from {table_2_choice}")

            if not selected_columns_1 or not selected_columns_2:
                messagebox.showerror("Error", "No columns selected in one of the tables.")
                return

            if len(selected_columns_1) != len(selected_columns_2):
                messagebox.showerror("Error", "Please select the same number of columns from both tables.")
                return

            compare_value = simpledialog.askstring("Input",
                                                   f"Enter the value to compare in columns {selected_columns_1} (Leave empty to compare all values):")

            common_matching_rows = process_multiple_tables(df_1_selected, df_2_selected, selected_columns_1, selected_columns_2, compare_value, progress_label)

            display_and_save(common_matching_rows)  # Display or save the results

        progress_window = tk.Toplevel()
        progress_window.title("Processing")
        progress_window.geometry("300x100")

        status_label = tk.Label(progress_window, text="Waiting for input...", width=40)
        status_label.pack(pady=20)

        progress_window.after(10, start_comparison)  # Start comparison after 10 ms

    start_comparison()
