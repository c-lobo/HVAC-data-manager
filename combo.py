import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText

GRAY = '#7A7675'
BLACK = '#17202A'
ORANGE = '#E0711E'
CREAM = '#DAD8B6'
BLUE = '#154776'
RED = '#B43C36'
GOLD = '#CEAA33'
WHITE = '#FBFCFC'

FONT = 'lexend'

class ComboFinder:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('esselogo.ico')
        self.root.title("Combo Finder")
        self.root.geometry('425x250')
        self.root.configure(bg=GRAY) 
        
        self.mainframe = tk.Frame(root, bg=CREAM)
        self.mainframe.pack(expand=True, fill='y')
        
        # Image properties
        img = Image.open("esselogo.png")   # 784x536
        resized = img.resize((40, 40), PIL.Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized)
        frame = tk.Label(self.mainframe, image=new_image, bg=CREAM)
        frame.image = new_image
        frame.grid(row=0, column=0, sticky='NE')
        
        self.label = tk.Label(
            self.mainframe, text="Combo Finder", font=(FONT, 16, 'bold'),
            bg=CREAM, fg=BLACK
        )
        self.label.grid(row=1, column=0, sticky='NEWS')
        
        self.colabel = tk.Label(
            self.mainframe, text='Enter Company', font=(FONT, 10, 'bold'),
            bg=CREAM, fg=BLACK
        )
        self.colabel.grid(row=2, column=0)
                   
        self.entry = tk.Entry(self.mainframe, bg='light blue')
        self.entry.grid(row=3, column=0)
        self.button = tk.Button(
            self.mainframe, text='get combo', font=(FONT, 10, 'bold'),
            bg=RED, fg=WHITE, command=self.get_combo, overrelief='sunken'
        )
        self.button.grid(row=4, column=0, pady=4)
        self.display = tk.Entry(self.mainframe, bg='light blue')
        self.display.grid(row=5, column=0)
            
        self.info = tk.Label(self.mainframe, text="""Enter companyA or companyB""", relief='groove', font=(FONT, 10, 'italic'), bg=CREAM, fg=BLACK)
        self.info.grid(row=6, column=0, pady=5)
        
    def get_combo(self):
        self.display.delete(0, tk.END)
        c = self.entry.get()
        
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Slim3!',
            database='sites'
        )    
        
        csr = conn.cursor()
        
        q1 = f"SELECT combo FROM lock_combo WHERE company = '{c}'"

        csr.execute(q1)
        
        self.display.insert(0, csr.fetchall())