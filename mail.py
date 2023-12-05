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

class Emailer:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('esselogo.ico')
        root.title('Parts Ordering')
        root.geometry('400x600')
        root.configure(bg=GRAY)
        
        self.mainframe = tk.Frame(root, bg=CREAM)
        self.mainframe.pack(expand=True, fill='y')
        
        # Image properties
        img = Image.open("esselogo.png")   # 784x536
        resized = img.resize((40, 40), PIL.Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized)
        frame = tk.Label(self.mainframe, image=new_image, bg=CREAM)
        frame.image = new_image
        frame.grid(row=0, column=1, sticky='SE', ipady=5)

        self.mainlabel = tk.Label(
            self.mainframe, bg=CREAM, fg=BLACK, font=(FONT, 16, 'bold', 'underline'),
            text='Parts Order Form')
        self.mainlabel.grid(row=1, column=0, columnspan=2, pady=20)
        
        self.vendorlabel = tk.Label(
            self.mainframe, text='ATT or VZW', bg=CREAM, fg=BLACK,
            font=(FONT, 10, 'bold', 'underline'))
        self.vendorlabel.grid(row=2, column=0)
        self.vendorbox = ttk.Combobox(self.mainframe, values=[' ', 'ATT', 'VZW'])
        self.vendorbox.grid(row=2, column=1, pady=10)
        
        self.nameLabel = tk.Label(
            self.mainframe, bg=CREAM, fg=BLACK,
            font=(FONT, 10, 'bold', 'underline'), text='Site Name')
        self.nameLabel.grid(row=3, column=0)
        
        self.nameEntry = tk.Entry(self.mainframe, bg='light blue')
        self.nameEntry.grid(row=3, column=1)
        
        self.idLabel = tk.Label(
            self.mainframe, bg=CREAM, fg=BLACK,
            font=(FONT, 10, 'bold', 'underline'), text='Site Id')
        self.idLabel.grid(row=4, column=0)
        
        self.idEntry = tk.Entry(self.mainframe, bg='light blue')
        self.idEntry.grid(row=4, column=1)
        
        self.modelLabel = tk.Label(
            self.mainframe, bg=CREAM, fg=BLACK, font=(FONT, 10, 'bold', 'underline'),
            text='Unit Model No.')
        self.modelLabel.grid(row=5, column=0)
        
        self.modelEntry = tk.Entry(self.mainframe, bg='light blue')
        self.modelEntry.grid(row=5, column=1)
        
        self.serialLabel = tk.Label(
            self.mainframe, bg=CREAM, fg=BLACK, font=(FONT, 10, 'bold', 'underline'),
            text='Unit Serial No.')
        self.serialLabel.grid(row=6, column=0)
        
        self.serialEntry = tk.Entry(self.mainframe, bg='light blue')
        self.serialEntry.grid(row=6, column=1)
        
        self.svcLabel = tk.Label(
            self.mainframe, bg=CREAM, fg=BLACK, font=(FONT, 10, 'bold', 'underline'),
            text='Job Number (SVC)')
        self.svcLabel.grid(row=7, column=0)
        
        self.svcEntry = tk.Entry(self.mainframe, bg='light blue')
        self.svcEntry.grid(row=7, column=1)
        
        self.quantityLabel = tk.Label(
            self.mainframe, bg=CREAM, fg=BLACK, font=(FONT, 10, 'bold', 'underline'),
            text='How Many Parts?')
        self.quantityLabel.grid(row=8, column=0, pady=5)
        
        self.quantity = tk.Spinbox(self.mainframe, from_=1, to=25)
        self.quantity.grid(row=9, column=0)
        
        self.button = tk.Button(
            self.mainframe, text='Input parts', relief='raised', font=(FONT, 10, 'bold'),
            bg=RED, fg=WHITE, command=self.parts_, overrelief='sunken')
        self.button.grid(row=10, column=0, pady=5)
        
        self.partsList = []

    def parts_(self):
    
        self.button.destroy()
        
        amount = int(self.quantity.get())
        for _ in range(amount):
            tk.Label(
                self.mainframe, bg=CREAM, fg=BLACK, font=(FONT, 10, 'bold'),
                text=f'Part {_+1}').grid(row=_+11, column=0)
            part = tk.Entry(self.mainframe, bg='light blue')
            part.grid(row=_+11, column=1, pady=5)
            
            self.partsList.append(part)

        self.button2 = tk.Button(
            self.mainframe, text='Send Email', relief='raised',
            font=(FONT, 10, 'bold'), bg=RED, fg=WHITE,
            command=self.send_mail, overrelief='sunken')
        self.button2.grid(row=_+2*amount+11, column=0, columnspan=3)

    def send_mail(self):

        vend = self.vendorbox.get()
        name = self.nameEntry.get()
        identify = self.idEntry.get()
        mod = self.modelEntry.get()
        ser = self.serialEntry.get()
        svc = self.svcEntry.get()
        parts = []
        for i in self.partsList:
            parts.append(i.get())

        self.vendorbox.set(" ")
        self.nameEntry.delete(0, tk.END)
        self.idEntry.delete(0, tk.END)
        self.modelEntry.delete(0, tk.END)
        self.serialEntry.delete(0, tk.END)
        self.svcEntry.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        [i.delete(0, tk.END) for i in self.partsList]

        sub = f"{vend} {name}"
        body = f"""
        Hello! I need to order {len(parts)} parts for the above mentioned site ({identify}),
        
        I need:
        {", ".join(parts)}
        
        for HVAC unit model no. {mod}
                      serial no. {ser}
                 
                 
        Job Number {svc}
        
        Thank You!
        """
        
        sender = 'kamrin717@gmail.com'
        rec = 'cameron.lopez@essellc.com'
        pw = 'iqqaadefxukffbff'
        
        msg = MIMEText(body)
        msg['Subject'] = sub
        msg['From'] = sender
        msg['To'] = rec
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, pw)
            server.sendmail(sender, rec, msg.as_string())
    
        messagebox.showinfo('Confirmed!', 'Email sent to parts department')