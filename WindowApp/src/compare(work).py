
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import file_handler
from fuzzywuzzy import fuzz
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
import queue
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


# Function to update progress bar
def update_progress(progress_label, message):
    progress_label.config(text=message)
    progress_label.update_idletasks()


# Handle matching for a single table based on user selection
def process_single_table(df_selected, selected_columns, compare_value, progress_label):
    # Filter data based on comparison value
    if compare_value:
        matching_rows = df_selected[df_selected[selected_columns[0]] == compare_value]
        for col in selected_columns[1:]:
            matching_rows = matching_rows[matching_rows[col] == compare_value]
    else:
        matching_rows = df_selected

    # Update progress as rows are processed
    update_progress(progress_label, f"Processed {len(matching_rows)} matching rows.")
    return matching_rows


# Handle matching between two tables based on user selection
def process_multiple_tables(df_1, df_2, selected_columns_1, selected_columns_2, compare_value, progress_label):
    # Track matched rows between the two dataframes
    matched_rows = []

    total_rows_1 = len(df_1)
    total_rows_2 = len(df_2)
    checked_rows_1 = 0
    checked_rows_2 = 0

    # Loop through both tables, row by row, and check for matches
    while checked_rows_1 < total_rows_1 or checked_rows_2 < total_rows_2:
        if checked_rows_1 < total_rows_1:
            df_1_row = df_1.iloc[checked_rows_1]
            checked_rows_1 += 1
        if checked_rows_2 < total_rows_2:
            df_2_row = df_2.iloc[checked_rows_2]
            checked_rows_2 += 1

        # Check if the selected columns match between the two rows
        if all(df_1_row[col_1] == df_2_row[col_2] for col_1, col_2 in zip(selected_columns_1, selected_columns_2)):
            matched_rows.append(df_1_row)  # Append matching row

        update_progress(progress_label, f"Processing rows {checked_rows_1}/{total_rows_1} (Table 1), {checked_rows_2}/{total_rows_2} (Table 2)")

    return pd.DataFrame(matched_rows)


# Function to display the results and ask user for saving
def display_and_save(matching_rows):
    if matching_rows.empty:
        messagebox.showinfo("No Matches", "No matching rows found based on your criteria.")
        return

    # Ask the user for the path to save the Excel file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")],
                                             title="Save Matching Rows")
    if file_path:
        try:
            # Save the DataFrame to an Excel file
            matching_rows.to_excel(file_path, index=False)
            messagebox.showinfo("File Saved", f"Matching data has been saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {e}")


def compare_data():
    def start_comparison():
        # Prompt user to select search mode (1 table or 2 tables)
        table_choice = simpledialog.askstring("Input",
                                              "Select the number of tables to search in (1 for searching within a single table, 2 for searching between two tables):")
        if table_choice not in ['1', '2']:
            messagebox.showerror("Error", "Please select either 1 or 2.")
            return

        # Function for searching within a single table
        def handle_single_table_search(progress_label):
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

            search_value = simpledialog.askstring("Input",
                                                 f"Enter the value to search in columns {selected_columns} (Leave empty to search all values):")

            matching_rows = search_single_table(df_selected, selected_columns, search_value, progress_label)

            display_and_save(matching_rows)  # Display or save the results

        # Function for searching between two tables
        def handle_multiple_table_search(progress_label):
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

            search_value = simpledialog.askstring("Input",
                                                 f"Enter the value to search in columns {selected_columns_1} (Leave empty to search all values):")

            common_matching_rows = search_multiple_tables(df_1_selected, df_2_selected, selected_columns_1, selected_columns_2, search_value, progress_label)

            display_and_save(common_matching_rows)  # Display or save the results

        # Progress window
        progress_window = tk.Toplevel()
        progress_window.title("Processing")
        progress_window.geometry("300x100")

        status_label = tk.Label(progress_window, text="Waiting for input...", width=40)
        status_label.pack(pady=20)

        # Based on the user's choice, either search within a single table or between tables
        if table_choice == '1':
            progress_window.after(10, lambda: handle_single_table_search(status_label))  # Start search for 1 table
        elif table_choice == '2':
            progress_window.after(10, lambda: handle_multiple_table_search(status_label))  # Start search for 2 tables

    start_comparison()  # Trigger the search process


# Function to search within a single table
from fuzzywuzzy import fuzz
import pandas as pd

def search_single_table(df_selected, selected_columns, search_value, progress_label):
    if search_value:
        # Convert the columns to string type before applying .str.contains()
        filtered_df = df_selected.copy()

        for col in selected_columns:
            filtered_df[col] = filtered_df[col].astype(str)  # Convert each column to string

        # Filter the rows based on the search value in the selected columns
        for col in selected_columns:
            filtered_df = filtered_df[filtered_df[col].str.contains(search_value, na=False, case=False)]  # case insensitive

        return filtered_df.drop_duplicates()
    else:
        # If no search value is provided, use fuzzy matching to find similar data
        matched_rows = []
        total_rows = len(df_selected)
        processed_rows = 0

        # Loop through each row in the dataframe
        for index, row in df_selected.iterrows():
            match = True
            for col in selected_columns:
                # Compare each value in the selected columns to the first value using fuzzy matching
                score = fuzz.ratio(row[col], row[selected_columns[0]])  # Compare each column with the first column value
                if score < 80:  # You can adjust this threshold for similarity
                    match = False
                    break
            if match:
                matched_rows.append(row)

            # Update progress after processing each row
            processed_rows += 1
            progress_label.config(text=f"Processing Row {processed_rows}/{total_rows}...")
            progress_label.update_idletasks()

        # Convert matched rows back to a DataFrame and drop duplicates
        common_matching_rows = pd.DataFrame(matched_rows).drop_duplicates()

        # Final progress update to indicate completion
        progress_label.config(text="Matching complete!")
        progress_label.update_idletasks()

        return common_matching_rows


import re

def clean_column_names(df):
    # Use regular expression to remove any spaces between characters
    df.columns = [re.sub(r'\s+', '', col) for col in df.columns]
    for col in df.columns:
        print(col)
    return df

def clean_selected_columns(selected_columns):
    # Clean the selected column names to ensure no spaces
    for col in selected_columns:
        print(col)
    return [re.sub(r'\s+', '', col) for col in selected_columns]



# Function to compare two rows (used for fuzzy matching)
def compare_rows(row_1, row_2, selected_columns_1, selected_columns_2):
    match = True
    for col_1, col_2 in zip(selected_columns_1, selected_columns_2):
        score = fuzz.ratio(row_1[col_1], row_2[col_2])  # Fuzzy matching score
        if score < 80:  # Set a threshold for similarity (80% similarity)
            match = False
            break
    return match

# Function to process matching with parallelization
def search_multiple_tables(df_1_selected, df_2_selected, selected_columns_1, selected_columns_2, search_value, progress_label):
    # Clean column names to remove spaces
    df_1_selected = clean_column_names(df_1_selected)
    df_2_selected = clean_column_names(df_2_selected)

    # Clean the selected columns to remove spaces
    selected_columns_1 = clean_selected_columns(selected_columns_1)
    selected_columns_2 = clean_selected_columns(selected_columns_2)

    # Ensure that the selected columns exist in the dataframe
    for col in selected_columns_1:
        if col not in df_1_selected.columns:
            raise KeyError(f"Column '{col}' not found in Table 1")

    for col in selected_columns_2:
        if col not in df_2_selected.columns:
            raise KeyError(f"Column '{col}' not found in Table 2")

    # Convert the columns to string type before applying .str.contains()
    for col in selected_columns_1:
        df_1_selected[col] = df_1_selected[col].astype(str)

    for col in selected_columns_2:
        df_2_selected[col] = df_2_selected[col].astype(str)

    # If no search_value is provided, perform fuzzy matching
    if not search_value:
        # Initialize progress queue
        progress_queue = queue.Queue()
        total_comparisons = len(df_1_selected) * len(df_2_selected)

        # Initialize tqdm for progress tracking
        progress_bar = tqdm(total=total_comparisons, desc="Processing matches", ncols=100)

        # Define a function for processing matches and updating progress
        def process_row_pair(row_1, row_2):
            match = compare_rows(row_1, row_2, selected_columns_1, selected_columns_2)
            progress_queue.put(1)  # Signal progress
            return match

        # Prepare the data for parallelization
        comparisons = [
            (row_1, row_2)
            for _, row_1 in df_1_selected.iterrows()
            for _, row_2 in df_2_selected.iterrows()
        ]

        # Parallelize fuzzy matching and handle progress
        matched_rows = Parallel(n_jobs=-1)(  # Use multiple cores for faster computation
            delayed(process_row_pair)(row_1, row_2) for row_1, row_2 in comparisons
        )

        # Collect progress updates and update progress bar
        processed_comparisons = 0
        while processed_comparisons < total_comparisons:
            progress_queue.get()  # Wait for a progress update
            processed_comparisons += 1
            progress_bar.update(1)  # Update the progress bar

        # Filter out the matches based on fuzzy matching
        matched_rows = [row_1 for row_1, match in zip(df_1_selected.iterrows(), matched_rows) if match]

        # Convert matched rows to DataFrame
        common_matching_rows = pd.DataFrame(matched_rows)

        # Close the progress bar
        progress_bar.close()

    else:
        # If search_value is provided, perform exact matching (same as before)
        filtered_df_1 = df_1_selected[df_1_selected[selected_columns_1[0]].str.contains(search_value, na=False, case=False)]
        for col in selected_columns_1[1:]:
            filtered_df_1 = filtered_df_1[filtered_df_1[col].str.contains(search_value, na=False, case=False)]

        filtered_df_2 = df_2_selected[df_2_selected[selected_columns_2[0]].str.contains(search_value, na=False, case=False)]
        for col in selected_columns_2[1:]:
            filtered_df_2 = filtered_df_2[filtered_df_2[col].str.contains(search_value, na=False, case=False)]

        # Merge the filtered rows from both tables on the selected columns
        common_matching_rows = pd.merge(filtered_df_1, filtered_df_2, left_on=selected_columns_1, right_on=selected_columns_2)

    # Drop duplicate rows in the merged dataframe
    common_matching_rows = common_matching_rows.drop_duplicates()

    # Final progress update to indicate completion
    progress_label.config(text="Matching complete!")
    progress_label.update_idletasks()

    return common_matching_rows
