import tkinter as tk
from tkinter import scrolledtext
import pyperclip

def generate_playfair_matrix(key): 
    key = "".join(dict.fromkeys(key))
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&'()*+,-./:;<=>?@[]^_`{|}~"
    matrix = [['' for _ in range(8)] for _ in range(8)]

    key_position = 0
    for row in range(8):
        for col in range(8):
            if key_position < len(key):
                matrix[row][col] = key[key_position]
                key_position += 1
            else:
                while True:
                    letter = alphabet[0]
                    alphabet = alphabet[1:] + letter
                    if letter not in key:
                        matrix[row][col] = letter
                        break

    return matrix

def find_position(matrix, char):
    for row in range(8):
        for col in range(8):
            if matrix[row][col] == char:
                return row, col
    return None

def playfair_encrypt(plaintext, key):
    matrix = generate_playfair_matrix(key)


    if len(plaintext) % 2 != 0:
        plaintext += 'X'

    ciphertext = ""

    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i + 1]
        position_a = find_position(matrix, a)
        position_b = find_position(matrix, b)

        if position_a is not None and position_b is not None:
            row_a, col_a = position_a
            row_b, col_b = position_b

            if row_a == row_b:
                ciphertext += matrix[row_a][(col_a + 1) % 8]
                ciphertext += matrix[row_b][(col_b + 1) % 8]
            elif col_a == col_b:
                ciphertext += matrix[(row_a + 1) % 8][col_a]
                ciphertext += matrix[(row_b + 1) % 8][col_b]
            else:
                ciphertext += matrix[row_a][col_b]
                ciphertext += matrix[row_b][col_a]
        else:
            print(f"Error: Character not found in matrix - {a}, {b}")

    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)

    if len(ciphertext) % 2 != 0:
        ciphertext += 'X'

    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        position_a = find_position(matrix, a)
        position_b = find_position(matrix, b)

        if position_a is not None and position_b is not None:
            row_a, col_a = position_a
            row_b, col_b = position_b

            if row_a == row_b:
                plaintext += matrix[row_a][(col_a - 1) % 8]
                plaintext += matrix[row_b][(col_b - 1) % 8]
            elif col_a == col_b:
                plaintext += matrix[(row_a - 1) % 8][col_a]
                plaintext += matrix[(row_b - 1) % 8][col_b]
            else:
                plaintext += matrix[row_a][col_b]
                plaintext += matrix[row_b][col_a]
        else:
            print(f"Error: Character not found in matrix - {a}, {b}")

    return plaintext

def copy_to_clipboard(text):
    pyperclip.copy(text)

def update_playfair_matrix_text(matrix_text, text_widget):
    text_widget.config(state='normal')
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, matrix_text)
    text_widget.config(state='disabled')

def encrypt_decrypt_button_click(action, matrix_text_widget, output_text_widget):
    key = key_entry.get().upper()
    input_text = input_text_entry.get().upper()
    matrix = generate_playfair_matrix(key)

    if action == "Encrypt":
        output_text = playfair_encrypt(input_text, key)
    elif action == "Decrypt":
        output_text = playfair_decrypt(input_text, key)

    matrix_text = "\n".join([" ".join(row) for row in matrix])
    update_playfair_matrix_text(matrix_text, matrix_text_widget)

    update_playfair_matrix_text(output_text, output_text_widget)
    copy_to_clipboard(output_text)

app = tk.Tk()
app.title("Playfair Cipher")
app.geometry("1280x720")

key_label = tk.Label(app, text="Key (Uppercase Letters, Digits, and Symbols):")
key_label.pack()
key_entry = tk.Entry(app, width=70)
key_entry.pack()

input_text_label = tk.Label(app, text="Input Text (Uppercase Letters, Digits, and Symbols):")
input_text_label.pack()
input_text_entry = tk.Entry(app, width=70)
input_text_entry.pack()

encrypt_button = tk.Button(app, text="Encrypt", command=lambda: encrypt_decrypt_button_click("Encrypt", playfair_matrix_text, output_text_text))
encrypt_button.pack()

decrypt_button = tk.Button(app, text="Decrypt", command=lambda: encrypt_decrypt_button_click("Decrypt", playfair_matrix_text, output_text_text))
decrypt_button.pack()

playfair_matrix_label = tk.Label(app, text="Playfair Matrix:")
playfair_matrix_label.pack()

playfair_matrix_text = scrolledtext.ScrolledText(app, height=10, width=70, wrap=tk.WORD)
playfair_matrix_text.pack()
playfair_matrix_text.config(state='disabled')

output_text_label = tk.Label(app, text="Output Text:")
output_text_label.pack()

output_text_text = scrolledtext.ScrolledText(app, height=10, width=70, wrap=tk.WORD)
output_text_text.pack()
output_text_text.config(state='disabled')

copy_button = tk.Button(app, text="Copy to Clipboard", command=lambda: copy_to_clipboard(output_text_text.get("1.0", tk.END)))
copy_button.pack()

app.mainloop()
