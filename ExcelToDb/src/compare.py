import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Function to retrieve table names from SQLite
def get_table_names(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

# Function to retrieve column names from a selected table
def get_column_names(table_name, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    conn.close()
    return [column[1] for column in columns]

# Function to compare the two selected tables and columns and display the result in a Treeview
def compare_data(db_file, table_combobox_1, table_combobox_2, column_combobox_1, column_combobox_2, value_entry):
    table_1 = table_combobox_1.get()
    table_2 = table_combobox_2.get()
    column_1 = column_combobox_1.get()
    column_2 = column_combobox_2.get()
    value = value_entry.get()

    # If no value is entered, compare the entire columns
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if value:
        # Query to compare selected values in both columns
        query = f"SELECT * FROM `{table_1}` t1 JOIN `{table_2}` t2 ON t1.`{column_1}` = t2.`{column_2}` WHERE t1.`{column_1}`=?"
        cursor.execute(query, (value,))
    else:
        # Query to compare entire columns
        query = f"SELECT * from `{table_1}` t1 JOIN `{table_2}` t2 ON t1.`{column_1}` = t2.`{column_2}`"
        cursor.execute(query)
    matched_data=cursor.fetchall()
    conn.close()
    return matched_data


