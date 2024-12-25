from tkinter import *
from tkinter import ttk
import pymupdf

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="PDF-Editor").grid(column=0, row=0)

doc = pymupdf.open("a.pdf")
for page in doc: 
    text_content = page.get_text().encode("utf8")
    ttk.Label(frm, text=text_content).grid(column=0, row=page.number)

root.mainloop()