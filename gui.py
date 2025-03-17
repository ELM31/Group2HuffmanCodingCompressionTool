import tkinter as tk
from tkinter import filedialog, messagebox
import os
from huffman import compress_file, decompress_file

stored_huffman_codes = None
stored_compressed_path = None

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        compress_and_display(file_path)

def compress_and_display(file_path):
    global stored_huffman_codes, stored_compressed_path
    compressed_path, huffman_codes = compress_file(file_path)
    
    original_size = os.path.getsize(file_path)
    compressed_size = os.path.getsize(compressed_path)
    compression_ratio = (compressed_size / original_size) * 100
    
    result_label.config(text=f"Original: {original_size} bytes | Compressed: {compressed_size} bytes | Ratio: {compression_ratio:.2f}%")
    huffman_codes_text.delete("1.0", tk.END)
    for char, code in huffman_codes.items():
        huffman_codes_text.insert(tk.END, f"{char}: {code}\n")
    
    stored_huffman_codes = huffman_codes
    stored_compressed_path = compressed_path

def decompress_and_display():
    if not stored_compressed_path or not stored_huffman_codes:
        messagebox.showerror("Error", "No file has been compressed yet!")
        return
    
    output_path = stored_compressed_path.replace(".bin", "_decompressed.txt")
    decompress_file(stored_compressed_path, stored_huffman_codes, output_path)
    with open(output_path, 'r', encoding='utf-8') as file:
        decoded_text = file.read()
    
    decoded_text_display.delete("1.0", tk.END)
    decoded_text_display.insert(tk.END, decoded_text)

# Tkinter GUI Setup
def launch_gui():
    global result_label, huffman_codes_text, decoded_text_display
    
    root = tk.Tk()
    root.title("Huffman Coding Compression Tool")
    root.configure(bg = '#140042')

    select_button = tk.Button(root, 
                              text="Select Text File", 
                              command=select_file,
                              fg='#c1bec8',
                              bg='#200067',
                              font=("Fixedsys", 17))
    select_button.pack()

    result_label = tk.Label(root,
                             text="Compression details will appear here.",
                             fg="#b550b2",
                             bg='#200067',
                             font=("Fixedsys", 2))
    result_label.pack()

    huffman_codes_text = tk.Text(root, 
                                 height=10, 
                                 width=50,
                                 fg = "#c1bec8",
                                 bg="#3b3b3b")
    huffman_codes_text.pack()

    decompress_button = tk.Button(root, 
                                  text="Decompress File", 
                                  command=decompress_and_display,
                                  fg="#c1bec8",
                                  bg="#200067",
                                  font=("Fixedsys", 17))
    decompress_button.pack()

    decoded_text_display = tk.Text(root, 
                                   height=10, 
                                   width=50, 
                                   fg = '#c1bec8',
                                   bg="#3b3b3b")
    decoded_text_display.pack()

    root.mainloop()
