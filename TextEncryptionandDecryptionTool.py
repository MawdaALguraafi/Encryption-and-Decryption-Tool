import customtkinter as ctk
import re

# Encrypt using  ROT13 
def encrypt_rot13(char):
    if char.isupper():
        return chr((ord(char) - 65 + 13) % 26 + 65)
    elif char.islower():
        return chr((ord(char) - 97 + 13) % 26 + 97)
    return char

#Decrypt using ROT13 
def decrypt_rot13(text):
    return ''.join(map(encrypt_rot13, text))

# Encrypt using Caesar Cipher
def encrypt_caesar(text, key):
    key = key % 26  

    def caesar_char(char):
        if char.isupper():  
            return chr((ord(char) - 65 + key) % 26 + 65)
        elif char.islower():  
            return chr((ord(char) - 97 + key) % 26 + 97)
        return char  

    return ''.join(map(caesar_char, text))

# Decrypt using Caesar Cipher
def decrypt_caesar(ciphertext, key):
    return encrypt_caesar(ciphertext, -key)

def process_cipher():
    text = input_text.get("1.0", ctk.END).strip()
    action = action_var.get()

    # Filter out texts with Arabic characters
    if any(re.search(r'[\u0600-\u06FF]', x) for x in text):
        output_entry.configure(state="normal")
        output_entry.delete("1.0", ctk.END)
        output_entry.insert("1.0", "Error: Input contains invalid characters.\nPlease use English characters.")
        output_entry.configure(state="disabled")
        return 
    

    if cipher_type.get() == "caesar":
        if not shift_key.get().isdigit():
            output_entry.configure(state="normal")
            output_entry.delete("1.0", ctk.END)
            output_entry.insert("1.0", "Error: Shift key must be a valid numeric value.")
            output_entry.configure(state="disabled")
            return


        key = int(shift_key.get())
        if action == "encrypt":
            result = encrypt_caesar(text, key)
        else:
            result = decrypt_caesar(text, key) 
    else:
        # Process ROT13
        if action == "encrypt":
            result = ''.join(map(encrypt_rot13, text))
        else:
            result = decrypt_rot13(text)

    # Display the result in the output 
    output_entry.configure(state="normal")
    output_entry.delete("1.0", ctk.END)
    output_entry.insert("1.0", result)
    output_entry.configure(state="disabled")

def show_cipher(type):
    cipher_type.set(type)
    shift_key_label.grid_forget()
    shift_key_entry.grid_forget()

    if hasattr(show_cipher, 'cipher_name_label'):
        show_cipher.cipher_name_label.grid_forget()

    cipher_name = f"{type.capitalize()} Cipher"
    show_cipher.cipher_name_label = ctk.CTkLabel(cipher_frame, text=cipher_name, font=("Arial", 16), text_color='white')
    show_cipher.cipher_name_label.grid(row=0, column=0, columnspan=2, pady=5)

    if type == "caesar":
        shift_key_label.grid(row=4, column=0, pady=5)
        shift_key_entry.grid(row=4, column=1, pady=5)

def go_back():
    cipher_frame.pack_forget()
    button_frame.pack(expand=True)

# Create main window
app = ctk.CTk()
app.title("Cipher Tool")
app.geometry("500x500")

# Create left and right rectangles
left_rectangle = ctk.CTkFrame(app, fg_color="#BCCBD6", width=100)
left_rectangle.pack(side=ctk.LEFT, fill=ctk.Y)

right_rectangle = ctk.CTkFrame(app, fg_color="#BCCBD6", width=100)
right_rectangle.pack(side=ctk.RIGHT, fill=ctk.Y)

# Initialize variables
cipher_type = ctk.StringVar()
action_var = ctk.StringVar(value="encrypt")
shift_key = ctk.StringVar(value="0")

# Create for buttons and cipher
main_frame = ctk.CTkFrame(app, fg_color="#1A2A44")
main_frame.pack(expand=True, fill=ctk.BOTH)

button_frame = ctk.CTkFrame(main_frame, fg_color="#1A2A44", corner_radius=8)
button_frame.pack(expand=True)

cipher_frame = ctk.CTkFrame(main_frame, fg_color="#1A2A44", corner_radius=8)


# Addlabel
ctk.CTkLabel(button_frame, text="Choose the encryption algorithm.", font=("Arial", 14), text_color='white').pack(pady=10)

# Create main buttons
ctk.CTkButton(button_frame, text="ROT13",
    command=lambda: [show_cipher("rot13"), button_frame.pack_forget(), cipher_frame.pack(expand=True)],
    font=("Arial", 14)).pack(side=ctk.LEFT, padx=10)

ctk.CTkButton(button_frame, text="Caesar Cipher",
    command=lambda: [show_cipher("caesar"), button_frame.pack_forget(), cipher_frame.pack(expand=True)],
    font=("Arial", 14)).pack(side=ctk.RIGHT, padx=10)
# Create input section with a Text 
ctk.CTkLabel(cipher_frame, text="Input:", font=("Arial", 12), text_color='white').grid(row=1, column=0, columnspan=2, pady=5)
input_text = ctk.CTkTextbox(cipher_frame, font=("Arial", 12), width=250, height=70, fg_color="#BCCBD6", text_color='black')
input_text.grid(row=2, column=0, columnspan=2, pady=5)

# Create buttons
ctk.CTkRadioButton(cipher_frame, text="Encrypt", variable=action_var, value="encrypt",
    font=("Arial", 12)).grid(row=3, column=0, pady=5)
ctk.CTkRadioButton(cipher_frame, text="Decrypt", variable=action_var, value="decrypt",
    font=("Arial", 12)).grid(row=3, column=1, pady=5)

# Create shift key section for Caesar cipher
shift_key_label = ctk.CTkLabel(cipher_frame, text="Shift Key:", font=("Arial", 12), text_color='white')
shift_key_entry = ctk.CTkEntry(cipher_frame, textvariable=shift_key, font=("Arial", 12))

# Create process button
ctk.CTkButton(cipher_frame, text="Process", command=process_cipher,
    font=("Arial", 12)).grid(row=5, column=0, columnspan=2, pady=5)

# Create output section with a Text
ctk.CTkLabel(cipher_frame, text="Output:", font=("Arial", 12), text_color='white').grid(row=6, column=0, columnspan=2, pady=5)
output_entry = ctk.CTkTextbox(cipher_frame, font=("Arial", 12), width=250, height=70, state="disabled", fg_color="#BCCBD6", text_color='black')
output_entry.grid(row=7, column=0, columnspan=2, pady=5)

# Create back button
ctk.CTkButton(cipher_frame, text="Back", command=go_back,
    font=("Arial", 12)).grid(row=8, column=0, columnspan=2, pady=5)

# Start the application
app.mainloop()
