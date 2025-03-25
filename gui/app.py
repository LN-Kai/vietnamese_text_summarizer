import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

from summarizer.summarizer import VietnameseTextSummarizer
from utils.file_handler import load_text_file

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vietnamese Text Summarizer")
        self.geometry("800x600")
        
        # Khởi tạo summarizer
        self.summarizer = VietnameseTextSummarizer()
        
        # Tạo widgets
        self.create_widgets()
    
    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label cho ô nhập văn bản
        input_label = tk.Label(main_frame, text="Nhập văn bản cần tóm tắt:")
        input_label.pack(anchor=tk.W)
        
        # Ô nhập văn bản
        self.text_input = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15)
        self.text_input.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Frame chứa nút và điều khiển
        control_frame = tk.Frame(main_frame)
        control_frame.pack(pady=10, fill=tk.X)
        
        # Nút tải file
        self.btn_load = tk.Button(control_frame, text="Tải file .txt", command=self.load_file)
        self.btn_load.pack(side=tk.LEFT, padx=5)
        
        # Ô nhập số cụm
        self.cluster_label = tk.Label(control_frame, text="Số cụm:")
        self.cluster_label.pack(side=tk.LEFT, padx=5)
        self.cluster_entry = tk.Spinbox(control_frame, from_=1, to=10, width=5)
        self.cluster_entry.pack(side=tk.LEFT, padx=5)
        self.cluster_entry.delete(0, "end")
        self.cluster_entry.insert(0, "3")  # Giá trị mặc định
        
        # Nút tóm tắt
        self.btn_summarize = tk.Button(control_frame, text="Tóm tắt", command=self.run_summarize)
        self.btn_summarize.pack(side=tk.LEFT, padx=5)
        
        # Nút xóa
        self.btn_clear = tk.Button(control_frame, text="Xóa tất cả", command=self.clear_all)
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Khu vực hiển thị kết quả
        result_label = tk.Label(main_frame, text="Bản tóm tắt:")
        result_label.pack(anchor=tk.W, pady=5)
        
        self.text_output = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=10)
        self.text_output.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Sẵn sàng")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filepath:
            try:
                content, encoding = load_text_file(filepath)
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(tk.END, content)
                self.status_var.set(f"Đã tải file ({encoding}): {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def run_summarize(self):
        input_text = self.text_input.get(1.0, tk.END).strip()
        if not input_text:
            messagebox.showerror("Lỗi", "Vui lòng nhập văn bản hoặc tải file!")
            return
        
        try:
            self.status_var.set("Đang xử lý...")
            self.update_idletasks()  # Cập nhật UI
            
            n_clusters = int(self.cluster_entry.get())
            summary = self.summarizer.summarize(input_text, n_clusters)
            
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, summary)
            
            if "Lỗi" in summary:
                self.status_var.set("Xảy ra lỗi khi tóm tắt")
            else:
                self.status_var.set(f"Đã tóm tắt thành công với {n_clusters} cụm")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi xử lý: {str(e)}")
            self.status_var.set("Xảy ra lỗi")
    
    def clear_all(self):
        self.text_input.delete(1.0, tk.END)
        self.text_output.delete(1.0, tk.END)
        self.cluster_entry.delete(0, "end")
        self.cluster_entry.insert(0, "3")
        self.status_var.set("Đã xóa tất cả")