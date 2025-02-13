import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import cv2
import os
from pathlib import Path

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")
        
        self.img_path = None
        self.char_to_int = {chr(i): i for i in range(255)}
        self.int_to_char = {i: chr(i) for i in range(255)}
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#2C3E50')
        self.style.configure('Custom.TButton', 
                           padding=10, 
                           font=('Helvetica', 12))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self.root, style='Custom.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with better styling
        title_frame = ttk.Frame(main_container, style='Custom.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(title_frame, 
                        text="Secure Image Steganography", 
                        font=("Helvetica", 24, "bold"),
                        bg="#2C3E50",
                        fg="#ECF0F1")
        title.pack()
        
        subtitle = tk.Label(title_frame,
                          text="Hide your secret messages in images",
                          font=("Helvetica", 12),
                          bg="#2C3E50",
                          fg="#BDC3C7")
        subtitle.pack()
        
        # Left panel for input controls
        left_panel = ttk.Frame(main_container, style='Custom.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Image selection section
        img_frame = tk.LabelFrame(left_panel, 
                                text="Image Selection",
                                font=("Helvetica", 12, "bold"),
                                bg="#34495E",
                                fg="#ECF0F1",
                                padx=10,
                                pady=10)
        img_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.img_path_label = tk.Label(img_frame,
                                     text="No image selected",
                                     bg="#34495E",
                                     fg="#BDC3C7",
                                     wraplength=300)
        self.img_path_label.pack(fill=tk.X, pady=(0, 5))
        
        select_btn = tk.Button(img_frame,
                             text="Select Image",
                             command=self.select_image,
                             bg="#27AE60",
                             fg="white",
                             font=("Helvetica", 11),
                             padx=20,
                             pady=5)
        select_btn.pack()
        
        # Message input section
        msg_frame = tk.LabelFrame(left_panel,
                                text="Message Input",
                                font=("Helvetica", 12, "bold"),
                                bg="#34495E",
                                fg="#ECF0F1",
                                padx=10,
                                pady=10)
        msg_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Message Entry as Text widget instead of Entry
        self.msg_entry = tk.Text(msg_frame,
                               width=40,
                               height=4,
                               font=("Helvetica", 11),
                               wrap=tk.WORD)
        self.msg_entry.pack(fill=tk.X, pady=(0, 5))
        
        load_text_btn = tk.Button(msg_frame,
                                text="Load from File",
                                command=self.load_text_file,
                                bg="#8E44AD",
                                fg="white",
                                font=("Helvetica", 11),
                                padx=20,
                                pady=5)
        load_text_btn.pack()
        
        # Password section
        pass_frame = tk.LabelFrame(left_panel,
                                 text="Security",
                                 font=("Helvetica", 12, "bold"),
                                 bg="#34495E",
                                 fg="#ECF0F1",
                                 padx=10,
                                 pady=10)
        pass_frame.pack(fill=tk.X)
        
        self.pass_entry = tk.Entry(pass_frame,
                                 show="•",
                                 font=("Helvetica", 11),
                                 width=30)
        self.pass_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Right panel for output and actions
        right_panel = ttk.Frame(main_container, style='Custom.TFrame')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Action buttons
        action_frame = tk.Frame(right_panel, bg="#2C3E50")
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        encode_btn = tk.Button(action_frame,
                             text="Encode Message",
                             command=self.encode_message,
                             bg="#2980B9",
                             fg="white",
                             font=("Helvetica", 11, "bold"),
                             padx=20,
                             pady=10)
        encode_btn.pack(side=tk.LEFT, padx=5)
        
        decode_btn = tk.Button(action_frame,
                             text="Decode Message",
                             command=self.decode_message,
                             bg="#E67E22",
                             fg="white",
                             font=("Helvetica", 11, "bold"),
                             padx=20,
                             pady=10)
        decode_btn.pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = tk.LabelFrame(right_panel,
                                   text="Decoded Message",
                                   font=("Helvetica", 12, "bold"),
                                   bg="#34495E",
                                   fg="#ECF0F1",
                                   padx=10,
                                   pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.decoded_text = tk.Text(output_frame,
                                  font=("Helvetica", 11),
                                  wrap=tk.WORD,
                                  bg="#ECF0F1",
                                  fg="#2C3E50")
        self.decoded_text.pack(fill=tk.BOTH, expand=True)
        self.decoded_text.config(state=tk.DISABLED)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root,
                            textvariable=self.status_var,
                            bg="#34495E",
                            fg="#ECF0F1",
                            pady=5)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_image(self):
        self.img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if self.img_path:
            self.img_path_label.config(text=f"Selected: {os.path.basename(self.img_path)}")
            self.status_var.set("Image loaded successfully")
    
    def load_text_file(self):
        """Load secret message from a text file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_content = file.read()
                    self.msg_entry.delete(1.0, tk.END)  # Clear current entry
                    self.msg_entry.insert(1.0, text_content)  # Insert text from file
                messagebox.showinfo("Success", "Text file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read text file: {str(e)}")
    
    def encode_message(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        msg = self.msg_entry.get("1.0", tk.END).strip()  # Get text from Text widget
        password = self.pass_entry.get()
        
        if not msg or not password:
            messagebox.showerror("Error", "Please enter both message and password!")
            return
            
        # Check if message is too long for the image
        try:
            img = cv2.imread(self.img_path)
            if img is None:
                raise Exception("Could not read image")
            
            max_bytes = img.shape[0] * img.shape[1] * 3 // 8  # Maximum bytes we can encode
            if len(msg) > max_bytes - 1:  # -1 for the length storage
                messagebox.showerror("Error", 
                    f"Message is too long! Maximum {max_bytes - 1} characters allowed for this image.")
                return
                
            # Store message length at the beginning
            msg_length = len(msg)
            img[0, 0, 0] = msg_length  # Store length in first pixel
            
            # Encode message starting from second pixel
            n, m, z = 1, 0, 0  # Start from next row
            for char in msg:
                if n >= img.shape[0] or m >= img.shape[1]:
                    raise Exception("Image too small for the message")
                img[n, m, z] = self.char_to_int[char]
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3
            
            # Save encoded image
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png")])
            if save_path:
                cv2.imwrite(save_path, img)
                messagebox.showinfo("Success", "Message encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def decode_message(self):
        if not self.img_path:
            messagebox.showerror("Error", "Please select an image first!")
            return
            
        password = self.pass_entry.get()
        if not password:
            messagebox.showerror("Error", "Please enter the password!")
            return
            
        try:
            img = cv2.imread(self.img_path)
            if img is None:
                raise Exception("Could not read image")
                
            # Get message length from first pixel
            msg_length = int(img[0, 0, 0])
            
            # Decode message starting from second pixel
            message = ""
            n, m, z = 1, 0, 0  # Start from next row
            for _ in range(msg_length):
                if n >= img.shape[0] or m >= img.shape[1]:
                    raise Exception("Message appears to be corrupted")
                message += self.int_to_char[int(img[n, m, z])]
                m += 1
                if m >= img.shape[1]:
                    m = 0
                    n += 1
                z = (z + 1) % 3
            
            # Update the text area with decoded message
            self.decoded_text.config(state=tk.NORMAL)  # Enable editing temporarily
            self.decoded_text.delete(1.0, tk.END)  # Clear previous content
            self.decoded_text.insert(tk.END, message)  # Insert new message
            self.decoded_text.config(state=tk.DISABLED)  # Make read-only again
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop() 