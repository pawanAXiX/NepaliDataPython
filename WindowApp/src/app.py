import tkinter as tk
from tkinter import filedialog, messagebox
from file_handler import upload_file  # Import the unified upload function
from compare import compare_data  # Import the compare function

# Function to display the data in the main window
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
    else:
        messagebox.showerror("Error", "Failed to upload the first file.")

upload_button_1 = tk.Button(root, text="Upload First Excel File", command=upload_first_file)
upload_button_1.pack(pady=10)

# Upload second file
def upload_second_file():
    file_path = upload_file(2)  # Assuming upload_file() returns the file path
    if file_path:
        file_status_label.config(text=f"Second file uploaded: {file_path}")
    else:
        messagebox.showerror("Error", "Failed to upload the second file.")

upload_button_2 = tk.Button(root, text="Upload Second Excel File", command=upload_second_file)
upload_button_2.pack(pady=10)

# Compare Data Button
def compare_button_pressed():
    try:
        compare_data()  # Assuming compare_data does the comparison logic
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during comparison: {e}")

compare_button = tk.Button(root, text="Compare Data", command=compare_button_pressed)
compare_button.pack(pady=10)

# Handle window close event
def on_closing():
    # This function is called when the close button is clicked
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()  # Close the window and terminate the program


root.protocol("WM_DELETE_WINDOW", on_closing)
# if display.check==True:
#     root.destroy()



# Start the Tkinter main loop
root.mainloop()
