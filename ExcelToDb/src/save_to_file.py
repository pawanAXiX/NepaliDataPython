import openpyxl


def save_fetchall_to_excel(data, column_names, filename="output.xlsx"):
    """
    Saves fetched database data to an Excel file.

    :param data: List of tuples (results from cursor.fetchall())
    :param column_names: List of column names (cursor.description)
    :param filename: Name of the output Excel file (default: output.xlsx)
    """
    if not data:
        print("No data to save.")
        return

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(column_names)  # Write header row

    for row in data:
        sheet.append(row)  # Write data rows

    workbook.save(filename)
    print(f"Data successfully saved to {filename}")
