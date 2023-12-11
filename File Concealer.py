# File Concealer & Decryptor App
#
# This program serves two main functions:
# 1. Concealing files within an image: Users can select a ZIP file, an image file, and an output directory.
#    The program will embed the ZIP file within the image file and save the result as a new image.
# 2. Decrypting concealed files from an image: Users can select a concealed image file and an output directory.
#    The program will extract concealed ZIP data from the image and save it as a ZIP file in the output directory.
#
# Features:
# - Users can select a ZIP file and an image file for concealment.
# - Users can select a concealed image file for decryption.
# - Users can specify output directories for both concealment and decryption.
# - Error messages are displayed if any issues occur during the concealment or decryption process.
#
# How to Use:
# - Run the program, and a GUI window will appear.
#
# - Conceal Section:
#   1. Select a ZIP file using the "Browse" button.
#   2. Select an image file using the "Browse" button.
#   3. Select an output directory using the "Browse" button.
#   4. Click the "Conceal Files" button to embed the ZIP file within the image.
#   5. Success or error messages will be displayed.
#
# - Decrypt Section:
#   1. Select a concealed image file using the "Browse" button.
#   2. Select an output directory using the "Browse" button.
#   3. Click the "Decrypt Files" button to extract concealed ZIP data from the image.
#   4. Success or error messages will be displayed.
#
# Note:
# - This program is designed for basic file concealment and decryption tasks.
# - Concealed files are embedded in PNG images.
# - Be cautious when using the concealment and decryption features, as data loss may occur.
#
# - Written by CodeKokeshi - August 15, 2023

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import shutil

# Function to select a ZIP file for concealment
def select_zip_file():
    file_path = filedialog.askopenfilename(filetypes=[("Zip Files", "*.zip")])
    if file_path:
        zip_file_entry.delete(0, tk.END)
        zip_file_entry.insert(tk.END, file_path)

# Function to select an image file for concealment
def select_image_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    if file_path:
        image_file_entry.delete(0, tk.END)
        image_file_entry.insert(tk.END, file_path)

# Function to select an output directory for concealment
def select_output_directory_conceal():
    directory_path = filedialog.askdirectory()
    if directory_path:
        output_dir_entry_conceal.delete(0, tk.END)
        output_dir_entry_conceal.insert(tk.END, directory_path)

# Function to conceal files within an image
def conceal_files():
    zip_file_path = zip_file_entry.get()
    image_file_path = image_file_entry.get()
    output_directory = output_dir_entry_conceal.get()

    if zip_file_path and image_file_path and output_directory:
        try:
            # Open the image and ZIP files
            with open(image_file_path, 'rb') as img_file, open(zip_file_path, 'rb') as zip_file:
                output_image_path = f"{output_directory}/output.png"
                # Create a new image by copying the content of the image and ZIP file into it
                with open(output_image_path, 'wb') as output_file:
                    shutil.copyfileobj(img_file, output_file)
                    shutil.copyfileobj(zip_file, output_file)

            info_label_conceal.config(text="Files concealed successfully!", fg="green")
        except Exception as e:
            info_label_conceal.config(text=f"Error: {str(e)}", fg="red")
    else:
        info_label_conceal.config(text="Please select all three files/directories.", fg="red")

# Function to select a concealed image file for decryption
def select_concealed_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    if file_path:
        concealed_file_entry.delete(0, tk.END)
        concealed_file_entry.insert(tk.END, file_path)

# Function to select an output directory for decryption
def select_output_directory_decrypt():
    directory_path = filedialog.askdirectory()
    if directory_path:
        output_dir_entry_decrypt.delete(0, tk.END)
        output_dir_entry_decrypt.insert(tk.END, directory_path)

# Function to decrypt files concealed within an image
def decrypt_files():
    concealed_file_path = concealed_file_entry.get()
    output_directory = output_dir_entry_decrypt.get()

    if concealed_file_path and output_directory:
        try:
            with open(concealed_file_path, 'rb') as concealed_file:
                # Locate the start position of the ZIP file within the output image
                zip_start = concealed_file.read().find(b'\x50\x4b\x03\x04')  # ZIP file signature
                if zip_start == -1:
                    raise ValueError("Concealed ZIP file not found in the image.")

                # Extract the concealed ZIP data
                concealed_file.seek(zip_start)
                zip_data = concealed_file.read()

                # Save the extracted data as a ZIP file
                output_zip_path = f"{output_directory}/extracted.zip"
                with open(output_zip_path, 'wb') as output_file:
                    output_file.write(zip_data)

            info_label_decrypt.config(text="Files decrypted successfully!", fg="green")
        except Exception as e:
            info_label_decrypt.config(text=f"Error: {str(e)}", fg="red")
    else:
        info_label_decrypt.config(text="Please select the concealed file and output directory.", fg="red")

# Create the main tkinter application window
app = tk.Tk()
app.title("File Concealer & Decryptor App")
app.geometry("400x550")
app.resizable(False, False)

# Label for Conceal section
conceal_label = tk.Label(app, text="Conceal Section", font=("Helvetica", 12, "bold"))
conceal_label.pack(pady=10)

# Conceal Section
zip_file_label = tk.Label(app, text="Select Zip File:")
zip_file_label.pack()

zip_file_entry = tk.Entry(app, width=50 )
zip_file_entry.pack()

zip_file_button = tk.Button(app, text="Browse", command=select_zip_file)
zip_file_button.pack()

image_file_label = tk.Label(app, text="Select Image File:")
image_file_label.pack()

image_file_entry = tk.Entry(app, width=50 )
image_file_entry.pack()

image_file_button = tk.Button(app, text="Browse", command=select_image_file)
image_file_button.pack()

output_dir_label_conceal = tk.Label(app, text="Select Output Directory:")
output_dir_label_conceal.pack()

output_dir_entry_conceal = tk.Entry(app, width=50 )
output_dir_entry_conceal.pack()

output_dir_button_conceal = tk.Button(app, text="Browse", command=select_output_directory_conceal)
output_dir_button_conceal.pack()

conceal_button = tk.Button(app, text="Conceal Files", command=conceal_files)
conceal_button.pack()

info_label_conceal = tk.Label(app, text="", fg="black")
info_label_conceal.pack()

# Add Separator
separator = ttk.Separator(app, orient="horizontal")
separator.pack(fill="x", padx=10, pady=10)

# Label for Decrypt section
decrypt_label = tk.Label(app, text="Decrypt Section", font=("Helvetica", 12, "bold"))
decrypt_label.pack(pady=10)

# Decrypt Section
concealed_file_label = tk.Label(app, text="Select Concealed File:")
concealed_file_label.pack()

concealed_file_entry = tk.Entry(app, width=50 )
concealed_file_entry.pack()

concealed_file_button = tk.Button(app, text="Browse", command=select_concealed_file)
concealed_file_button.pack()

output_dir_label_decrypt = tk.Label(app, text="Select Output Directory:")
output_dir_label_decrypt.pack()

output_dir_entry_decrypt = tk.Entry(app, width=50 )
output_dir_entry_decrypt.pack()

output_dir_button_decrypt = tk.Button(app, text="Browse", command=select_output_directory_decrypt)
output_dir_button_decrypt.pack()

decrypt_button = tk.Button(app, text="Decrypt Files", command=decrypt_files)
decrypt_button.pack()

info_label_decrypt = tk.Label(app, text="", fg="black")
info_label_decrypt.pack()

# Start the tkinter event loop
app.mainloop()
