import cv2
import os
import string
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Initialize global variables for the image
img = None
msg = ""
password = ""
encrypted_img_path = "encryptedImage.jpg"

def open_image():
    global img
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")])
    if file_path:
        img = cv2.imread(file_path)
        display_image(file_path)

def display_image(img_path):
    # Display image in the GUI
    img_pil = Image.open(img_path)
    img_pil.thumbnail((300, 300))  # Resize the image for display purposes
    img_tk = ImageTk.PhotoImage(img_pil)

    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection

def encrypt_image():
    global img, msg, password
    msg = secret_msg_entry.get()
    password = passcode_entry.get()

    if not msg or not password or img is None:
        messagebox.showerror("Error", "Please fill in all fields and select an image.")
        return

    # Prepare the dictionary for encryption
    d = {}
    c = {}
    for i in range(255):
        d[chr(i)] = i
        c[i] = chr(i)

    n, m, z = 0, 0, 0

    # Encrypt the message into the image
    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n = n + 1
        m = m + 1
        z = (z + 1) % 3

    # Save the encrypted image
    cv2.imwrite(encrypted_img_path, img)
    os.system(f"start {encrypted_img_path}")  # Use 'start' to open the image on Windows

    messagebox.showinfo("Success", "Image has been encrypted and saved.")

def decrypt_image():
    global img, password, msg
    if img is None or not password:
        messagebox.showerror("Error", "Please select an image and enter the passcode.")
        return

    pas = passcode_decrypt_entry.get()

    if password == pas:
        # Prepare the dictionary for decryption
        c = {}
        for i in range(255):
            c[i] = chr(i)

        # Decrypt the message
        message = ""
        n, m, z = 0, 0, 0
        for i in range(len(msg)):
            message = message + c[img[n, m, z]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3

        decrypted_message_label.config(text=f"Decrypted Message: {message}")
    else:
        messagebox.showerror("Error", "Incorrect passcode! Decryption failed.")

# Set up the main GUI window
root = tk.Tk()
root.title("Steganography")
root.geometry('400x450')

# Create GUI components
image_label = tk.Label(root)
image_label.grid(row=0, column=0, columnspan=3)

open_image_button = tk.Button(root, text="Open Image", command=open_image)
open_image_button.grid(row=1, column=0, columnspan=2)

secret_msg_label = tk.Label(root, text="Enter Secret Message:")
secret_msg_label.grid(row=2, column=0)

secret_msg_entry = tk.Entry(root)
secret_msg_entry.grid(row=2, column=1)

passcode_label = tk.Label(root, text="Enter Passcode:")
passcode_label.grid(row=3, column=0)

passcode_entry = tk.Entry(root, show="*")
passcode_entry.grid(row=3, column=1)

encrypt_button = tk.Button(root, text="Encrypt Image", command=encrypt_image)
encrypt_button.grid(row=4, column=0, columnspan=2)

passcode_decrypt_label = tk.Label(root, text="Enter Passcode for Decryption:")
passcode_decrypt_label.grid(row=5, column=0)

passcode_decrypt_entry = tk.Entry(root, show="*")
passcode_decrypt_entry.grid(row=5, column=1)

decrypt_button = tk.Button(root, text="Decrypt Image", command=decrypt_image)
decrypt_button.grid(row=6, column=0, columnspan=2)

decrypted_message_label = tk.Label(root, text="Decrypted Message: ")
decrypted_message_label.grid(row=7, column=0, columnspan=2)

# Start the GUI event loop
root.mainloop()
