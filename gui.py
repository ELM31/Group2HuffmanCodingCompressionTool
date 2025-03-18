import tkinter as tk                                #tkinter library for GUI
from tkinter import filedialog, messagebox          #Import filedialog to allow users to interact with their file system, message box for displaying separate message boxes
import os                                           #Operating System library used to help get size of files
from huffman import compress_file, decompress_file  #Needed functions from huffman python file 

stored_huffman_codes = None
stored_compressed_path = None

def select_file(): 
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]) #User chooses file
    if file_path: #if statement checks if file is non-void, allows the file to continue to the next function
        compress_and_display(file_path)

def compress_and_display(file_path):
    global stored_huffman_codes, stored_compressed_path 
    compressed_path, huffman_codes = compress_file(file_path) #compress file using function from huffman code 
    
    #getting the ratio 
    original_size = os.path.getsize(file_path) #return orignal file size in bytes
    compressed_size = os.path.getsize(compressed_path) #return compressed file size in bytes
    compression_ratio = (compressed_size / original_size) * 100 #percentage of compressed file size compared to the original file size 
    
    #Showing results 
    result_label.config(text=f"Original: {original_size} bytes | Compressed: {compressed_size} bytes | Ratio: {compression_ratio:.2f}%") #results of the compression
    huffman_codes_text.delete("1.0", tk.END) #gets rid of the previous label to show results
    
    #Go through the huffman_code dictonrary inserting each character into the huffman_code_text textbox
    for char, code in huffman_codes.items():
        huffman_codes_text.insert(tk.END, f"{char}: {code}\n")
    
    #storing into the global variables 
    stored_huffman_codes = huffman_codes
    stored_compressed_path = compressed_path


def decompress_and_display():
    #If program does has not yet used a file yet 
    if not stored_compressed_path or not stored_huffman_codes:
        messagebox.showerror("Error", "No file has been compressed yet!")
        return
    
    #Decompression processusing the decompress_file from the huffman python file 
    output_path = stored_compressed_path.replace(".bin", "_decompressed.txt")
    decompress_file(stored_compressed_path, stored_huffman_codes, output_path)
    
    #reading the decompressed file 
    with open(output_path, 'r', encoding='utf-8') as file:
        decoded_text = file.read()
    
    #Display text, while also deleting texts if any exists in the textbox
    decoded_text_display.delete("1.0", tk.END)
    decoded_text_display.insert(tk.END, decoded_text)

# Tkinter GUI Setup
def launch_gui():
    global result_label, huffman_codes_text, decoded_text_display
    
    #root
    root = tk.Tk()
    root.title("Huffman Coding Compression Tool")
    root.configure(bg = '#140042')

    #Widget properties for the Select button 
    select_button = tk.Button(root, 
                              text="Select Text File", 
                              command=select_file,
                              activebackground="#6a6a6a",
                              activeforeground="white",
                              fg='#c1bec8',
                              bg='#200067',
                              font=("Fixedsys", 17),
                              cursor="hand2",
                              bd=3,
                              disabledforeground="gray",
                              highlightbackground="black",
                              highlightcolor="green",
                              highlightthickness=2
                              )
    select_button.pack()

    #Widget properties for the results label 
    result_label = tk.Label(root,
                             text="Compression details will appear here.",
                             fg="#b550b2",
                             bg='#200067',
                             font=("Fixedsys", 2))
    result_label.pack()

    #Widget properties for the Huffman code textbox 
    huffman_codes_text = tk.Text(root, 
                                 height=10, 
                                 width=50,
                                 fg = "#c1bec8",
                                 bg="#585858")
    huffman_codes_text.pack()

    #Widget properties for the decompress button
    decompress_button = tk.Button(root, 
                                  text="Decompress File", 
                                  command=decompress_and_display,
                                  activebackground="#6a6a6a",
                                  activeforeground="white",
                                  fg='#c1bec8',
                                  bg='#200067',
                                  font=("Fixedsys", 17),
                                  cursor="hand2",
                                  bd=3,
                                  disabledforeground="gray",
                                  highlightbackground="black",
                                  highlightcolor="green",
                                  highlightthickness=2)
    decompress_button.pack()

    #Widget properties for the decoded textbox 
    decoded_text_display = tk.Text(root, 
                                   height=10, 
                                   width=50, 
                                   fg = '#c1bec8',
                                   bg="#585858")
    decoded_text_display.pack()

    root.mainloop()
