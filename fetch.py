import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
import input

# Color schema
GRAY = '#7A7675'
BLACK = '#17202A'
ORANGE = '#E0711E'
CREAM = '#DAD8B6'
BLUE = '#154776'
RED = '#B43C36'
GOLD = '#CEAA33'
WHITE = '#FBFCFC'

FONT = 'lexend'

class GetData:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('esselogo.ico')
        self.root.title('HVAC Data Retrieval')
        self.root.geometry('300x500')
        self.root.configure(bg=GRAY)
        
        self.mainframe = tk.Frame(root, bg=CREAM)
        self.mainframe.pack(expand=True, fill='y')
        
        # Image properties
        img = Image.open("esselogo.png")   # 784x536
        resized = img.resize((40, 40), PIL.Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized)
        frame = tk.Label(self.mainframe, image=new_image, bg=CREAM)
        frame.image = new_image
        frame.grid(row=0, column=1, sticky='NE', ipady=5)
        
        self.getLabel = (tk.Label(
            self.mainframe, text='Search Site Data',
            bg=CREAM, fg=BLACK, font=(FONT, 14, 'bold', 'underline')))
        self.getLabel.grid(row=1, column=0, columnspan=4, pady=3)
        
        labels = ['Site ID', 'Site Name'] 
        self.label_entries = {}
        
        for index, value in enumerate(labels):
            tk.Label(self.mainframe, text=value, bg=CREAM, fg=BLACK, font=(FONT, 12)).grid(row=index+2, column=0)
            entry = tk.Entry(self.mainframe, bg='light blue')
            entry.grid(row=index+2, column=1)
            self.label_entries[value] = entry
        self.button = (tk.Button(
            self.mainframe, command=self.show_info,
            text='Search', bg=RED, fg=CREAM, font=(FONT, 10, 'bold'),
            overrelief='sunken'))
        self.button.grid(row=len(self.label_entries)+2, column=0, columnspan=2)

    def show_info(self):

        headers = [
            "idx", 'Site ID', 'Site Name', 'Coordinates',
            'Tower Manager', 'Unit Make', 'Unit Model', 'Unit Serial',
            'Compressor', 'Outdoor Fan', 'Indoor Fan', 'BTU',
            'Freon', 'Controller', 'Filter Size'
        ]
                
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Slim3!',
            database='sites'
        )
        csr = conn.cursor()

        vals = []
        for i in self.label_entries.values():
            i = i.get()
            vals.append(i)
    
        if vals[0]: 
            csr.execute("SELECT * FROM site_master WHERE site_id = %s;" % (vals[0]))
            data = csr.fetchall()
            grid = []
            for i in data:
                grid.append(i)
            row = len(grid)
            col = len(grid[0])
            for r in range(row):
                for c in range(col):
                    self.e = tk.Entry(self.mainframe, bg='light blue', fg=BLACK)
                    self.e.grid(row=c+6, column=1)
                    self.e.insert(0, grid[r][c]) 
            for index, i in enumerate(headers):
                tk.Label(self.mainframe, text=i, bg=CREAM, fg=BLACK).grid(row=index+6, column=0)       
        elif vals[1]:
            csr.execute("SELECT * FROM site_master WHERE site_name = %s;" % ("'" + vals[1] + "'"))
            data = csr.fetchall()
            grid = []
            for i in data:
                grid.append(i)
            row = len(grid)
            col = len(grid[0])
            for r in range(row):
                for c in range(col):
                    self.e = tk.Entry(self.mainframe, bg='light blue', fg=BLACK)
                    self.e.grid(row=c+6, column=1)
                    self.e.insert(0, grid[r][c])
            for index, i in enumerate(headers):
                tk.Label(self.mainframe, text=i, bg=CREAM, fg=BLACK).grid(row=index+6, column=0)
        else:
            self.e.insert(tk.END, "Invalid Entry, Try Again.")