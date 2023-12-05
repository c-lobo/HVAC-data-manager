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

class InputData:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('esselogo.ico')
        self.root.title('HVAC data logger')
        self.root.geometry('350x600')
        self.root.configure(bg=GRAY)

        self.mainframe = tk.Frame(root, bg=CREAM)
        self.mainframe.pack(expand=True, fill='y')
        
        # Image properties
        img = Image.open("esselogo.png")   # 784x536
        resized = img.resize((40, 40), PIL.Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized)
        frame = tk.Label(self.mainframe, image=new_image, bg=CREAM)
        frame.image = new_image
        frame.grid(row=0, column=1, sticky='NE')
        
        self.main_label = (
            tk.Label(self.mainframe, text='Input Site Data', bg=CREAM,
                     fg=BLACK, font=(FONT, 14, 'bold', 'underline'))
        )

        self.main_label.grid(row=1, column=0, columnspan=4)

        labels = [
            'Site ID', 'Site Name', 'Coordinates', 'Site Owner',
            'Unit Make', 'Unit Model', 'Unit Serial', 'Compressor',
            'Outdoor Fan [rpm:hp]', 'Indoor Fan [rpm:hp]', 'Tons',
            'Freon', 'Controller', 'Filter Size']
        
        self.site_entries = {}
                
        for index, label in enumerate(labels):
            tk.Label(self.mainframe, text=label, bg=CREAM, fg=BLACK, font=(FONT, 12)).grid(row=index + 2, column=0)
            entry = tk.Entry(self.mainframe, bg='light blue')
            entry.grid(row=index + 2, column=1, padx=4, pady=2)
            self.site_entries[index] = entry 

        tk.Button(
            self.mainframe, text='Submit', command=self.input_data,
            borderwidth=5, relief='raised', font=(FONT, 10, 'bold'),
            bg=RED, fg=CREAM, overrelief='sunken').grid(row=len(labels) + 2, column=0, columnspan=4, pady=10)

    def input_data(self):

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Slim3!',
            database='sites'
        )    
        
        csr = conn.cursor()
        cols = [
            'site_id',  # 0
            'site_name',  # 1
            'coordinates',  # 2
            'owner',  # 3
            'manufacturer',  # 4
            'model_no',  # 5
            'serial_no',  # 6
            'compressor',   # 7
            'outdoor_fan',  # 8
            'indoor_fan',  # 9
            'tonnage',  # 10
            'freon',  # 11
            'controller',  # 12
            'filter_size'  # 13
        ]
        cols = ", ".join(cols)

        vals = []
        result = ""
        for e in self.site_entries.values():
            e = e.get()
            vals.append("'" + e + "'")  
            result += "'" + e + "'"
            
        [i.delete(0, tk.END) for i in self.site_entries.values()]       

        q1 = "INSERT INTO site_master (%s) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (cols, vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], vals[9], vals[10], vals[11], vals[12], vals[13])

        csr.execute(q1)
        conn.commit()
        conn.close()
        
        messagebox.showinfo('Submitted', 'Your data has been logged!')