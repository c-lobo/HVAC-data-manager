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

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title('HVAC Notepad')
        self.root.configure(bg=GRAY)
        self.root.iconbitmap('esselogo.ico')
        self.root.geometry('575x550')
        
        self.mainframe = tk.Frame(self.root, bg=CREAM)
        self.mainframe.pack()
        self.scrollbar = tk.Scrollbar(self.mainframe)
        self.scrollbar.pack(side='right', fill='y')
        
        img = Image.open('esselogo.png')
        resized = img.resize((40, 40), PIL.Image.Resampling.LANCZOS)
        new_img = ImageTk.PhotoImage(resized)
        picframe = tk.Label(self.mainframe, image=new_img, bg=CREAM)
        picframe.image = new_img
        picframe.pack(side='top', anchor='w')

        tk.Label(
            self.mainframe, text='Site Name', bg=CREAM,
            font=(FONT, 10, 'bold')).pack(ipady=2, side='top', anchor='e', padx=5)
        self.siteNameEntry = tk.Entry(self.mainframe)
        self.siteNameEntry.pack(side='top', anchor='e', padx=5)

        self.pad = tk.Text(
            self.mainframe, fg=BLACK, font=(FONT, 10),
            selectbackground=GOLD, selectforeground=WHITE,
            yscrollcommand=self.scrollbar.set, undo=True)
        self.pad.pack()
        self.scrollbar.config(command=self.pad.yview)

        self.myMenu = tk.Menu(self.root, bg=CREAM)
        self.root.config(menu=self.myMenu, bg=CREAM)
        
        self.fileMenu = tk.Menu(self.myMenu, tearoff=False)
        self.myMenu.add_cascade(label='File', menu=self.fileMenu)
        
        self.fileMenu.add_command(label='New', command=self.newFile)
        self.fileMenu.add_command(label='Open', command=self.openFile)
        self.fileMenu.add_command(label='Save', command=self.saveFile)
        self.fileMenu.add_command(label='Save As', command=self.saveasFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Close', command=self.root.quit)
        
        self.editMenu = tk.Menu(self.myMenu, tearoff=False)
        self.myMenu.add_cascade(label='Edit', menu=self.editMenu)
        
        self.editMenu.add_command(label='Cut', command=self.cutText)
        self.editMenu.add_command(label='Copy', command=self.copyText)
        self.editMenu.add_command(label='Paste', command=self.pasteText)
        self.editMenu.add_command(label='Undo', command=self.pad.edit_undo)
        self.editMenu.add_command(label='Redo', command=self.pad.edit_redo)
        
        self.sBar = tk.Label(self.root, text='Ready     ', anchor='e')
        self.sBar.pack(fill='x', side='bottom', ipady=5)

    def newFile(self):
        self.pad.delete(1.0, tk.END)
        self.sBar.config(text='New File     ')
        
    def openFile(self):
        self.pad.delete(1.0, tk.END)
        
        opened = filedialog.askopenfilename(
            initialdir='C:\\Users\\clopez\\OneDrive\\Desktop\\Notes\\personal notes\\App Notes'
        )
        name = opened
        self.sBar.config(text=name)
        
        opened = open(opened, 'r')
        o = opened.read()
        self.pad.insert(tk.END, o)

    def saveFile(self):
        saveName = self.siteNameEntry.get()
        openFile = open(f'C:\\Users\\clopez\\OneDrive\\Desktop\\Notes\\personal notes\\App Notes\\{saveName}', 'w')
        openFile.write(self.pad.get(1.0, tk.END))
        openFile.close()

    def saveasFile(self):
        openFile = filedialog.asksaveasfilename()
        openFile = open(openFile, 'w')
        openFile.write(self.pad.get(1.0, tk.END))
        openFile.close()

    def cutText(self):
        if self.pad.selection_get():
            self.sel = self.pad.selection_get()
            self.pad.delete('sel.first', 'sel.last')

    def copyText(self):
        if self.pad.selection_get():
            self.sel = self.pad.selection_get()
            
    def pasteText(self):
        if self.sel:
            self.pos = self.pad.index('insert')
            self.pad.insert(self.pos, self.sel)