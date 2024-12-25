import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import pymupdf
from pathlib import Path

class PDFViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Edible")
        self.setup_ui()
        self.current_page = 0
        self.doc = None

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Button(self.frame, text="Open PDF", command=self.open_pdf).grid(row=0, column=0, pady=5)
        self.page_label = ttk.Label(self.frame, text="Page: 0/0")
        self.page_label.grid(row=0, column=1, padx=5)
        ttk.Button(self.frame, text="Previous", command=self.prev_page).grid(row=0, column=2)
        ttk.Button(self.frame, text="Next", command=self.next_page).grid(row=0, column=3)

        self.text_area = scrolledtext.ScrolledText(self.frame, width=60, height=30)
        self.text_area.grid(row=1, column=0, columnspan=4, pady=5)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                self.doc = pymupdf.open(file_path)
                self.current_page = 0
                self.update_page()
                self.root.title(f"PDF Viewer - {Path(file_path).name}")
            except Exception as e:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f"Error opening PDF: {str(e)}")

    def update_page(self):
        if not self.doc:
            return
        
        self.page_label.config(text=f"Page: {self.current_page + 1}/{len(self.doc)}")
        self.text_area.delete(1.0, tk.END)
        
        try:
            page = self.doc[self.current_page]
            text = page.get_text()
            self.text_area.insert(tk.END, text)
        except Exception as e:
            self.text_area.insert(tk.END, f"Error reading page: {str(e)}")

    def next_page(self):
        if self.doc and self.current_page < len(self.doc) - 1:
            self.current_page += 1
            self.update_page()

    def prev_page(self):
        if self.doc and self.current_page > 0:
            self.current_page -= 1
            self.update_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFViewer(root)
    root.mainloop()
