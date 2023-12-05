import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import PIL
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
import input, fetch, combo, mail, noted

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

class Main:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap('esselogo.ico')
        root.title('HVAC main page')
        root.geometry('275x380')
        root.configure(bg=GRAY)

        self.mainframe = tk.Frame(root, bg=CREAM)
        self.mainframe.pack(expand=True, fill='y')
        
        self.label = tk.Label(
            self.mainframe, text='HVAC dashboard',
            bg=CREAM, fg=BLACK, font=(FONT, 16, 'bold', 'underline'))
        self.label.grid(row=1, column=0)
        
        self.inputButton = tk.Button(
            self.mainframe, text='Input HVAC data', command=self.inData, relief='raised',
            font=(FONT, 10, 'bold'), bg=RED, fg=WHITE, overrelief='sunken')
        self.inputButton.grid(row=2, column=0, pady=5)
        
        self.getButton = tk.Button(
            self.mainframe, text='Get HVAC data', command=self.getData,
            relief='raised', font=(FONT, 10, 'bold'),
            bg=RED, fg=WHITE, overrelief='sunken')
        self.getButton.grid(row=3, column=0, pady=5)
        
        self.comboButton = tk.Button(
            self.mainframe, text='Get Lock Combo', command=self.getCombo,
            relief='raised', font=(FONT, 10, 'bold'),
            bg=RED, fg=WHITE, overrelief='sunken')
        self.comboButton.grid(row=4, column=0, pady=5)
        
        self.emailButton = tk.Button(
            self.mainframe, text='Order Parts', command=self.emailParts,
            relief='raised', font=(FONT, 10, 'bold'),
            bg=RED, fg=WHITE, highlightcolor=CREAM, overrelief='sunken')
        self.emailButton.grid(row=5, column=0, pady=5)
         
        self.padButton = tk.Button(
            self.mainframe, text='Notepad', command=self.notepad,
            relief='raised', font=(FONT, 10, 'bold'),
            bg=RED, fg=WHITE, highlightcolor=CREAM, overrelief='sunken')
        self.padButton.grid(row=6, column=0, pady=5)
        
        # Image properties
        img = Image.open("esselogo.png")   # 784x536
        resized = img.resize((100, 100), PIL.Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized)
        frame = tk.Label(self.mainframe, image=new_image, bg=CREAM)
        frame.image = new_image
        frame.grid(row=0, column=0, pady=5)

    def inData(self):
        tl = tk.Toplevel(self.root)
        input.InputData(tl)

    def getData(self):
        tl = tk.Toplevel(self.root)
        fetch.GetData(tl)
        
    def getCombo(self):
        tl = tk.Toplevel(self.root)
        combo.ComboFinder(tl)
        
    def emailParts(self):
        tl = tk.Toplevel(self.root)
        mail.Emailer(tl)
        
    def notepad(self):
        tl = tk.Toplevel(self.root)
        noted.Notepad(tl)



if __name__ == '__main__':
    app = tk.Tk()
    Main(app)
    app.mainloop()
    
    