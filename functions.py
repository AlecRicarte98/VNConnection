import os
import subprocess
import sys
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import filedialog
from PIL import Image, ImageTk



class ButtonCell(tk.Button):
    def __init__(self, master=None, text="", command=None, **kwargs):
        tk.Button.__init__(self, master, text=text, command=command, **kwargs)
        self.config(justify='center')


class Table(tk.Frame):
    def __init__(self, master=None, rows=0, columns=0, data=None, external_value=None):
        tk.Frame.__init__(self, master, background='#697589')

        self.columns = columns
        self.cells = []

        # Agregar cabeceras de columna
        headers = ['Machine', 'IP Address', 'Location' , 'Leader', 'Connection State']
        header_row = []
        c = 0
        connect_btn_img = tk.PhotoImage(resource_path('images/connect_btn.png'))
        for j in headers:
            header_label = tk.Label(self, text=j, font=("Calibri", 20), fg='#FFFFFF', background='#697589')
            header_label.grid(row=0, column=c, padx=30)
            header_row.append(header_label)
            c = c+1
        self.cells.append(header_row)

        # Agregar filas de datos
        if data:
            for i, row_data in enumerate(data, start=1):
                data_row = []
                for j in range(columns):
                    if j == columns - 1:
                        cell = ButtonCell(self, image=connect_btn_img, command=lambda: connection(row_data[j], external_value, cell))
                        cell.config(justify='center')
                    else:
                        cell = tk.Label(self, text=row_data[j], font=("Calibri", 20), justify='center', fg='#FFFFFF', background='#697589')
                    cell.grid(row=i, column=j, padx=10)
                    data_row.append(cell)
                self.cells.append(data_row)








def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def readFile():
    file = open(resource_path('Clients.txt'))
    nameList = []
    for line in file:
        columns = line.split('\t')
        nameList.append(columns)
    return nameList

def fileselect(entry):
    file = filedialog.askopenfilename(filetypes=(('Virtual Network Computing files', '*.vnc'), ("All files", "*.*")))
    if file != "":
        entry.insert(0, file)

def connection(connname, ui, button):
    print(connname)
    file = open(resource_path('Clients.txt'))
    vncpath = connname
    if vncpath != '' and vncpath != 'No_path' and vncpath[-4:] == '.vnc':
        on_line_img = tk.PhotoImage(resource_path('images/on_line_btn.png'))
        button.image = on_line_img
        args = r"C:\Program Files (x86)\uvnc bvba\UltraVNC\vncviewer.exe -config " + vncpath
        subprocess.call(args)


    else:
        error = tk.Message(ui, text='Invalid VNC Path', font=('Calibri', 14),  fg='#FFFF00', background='#1C283A', width=200)
        error.place(relx=0.5, rely=0.85, anchor='center')
        error.after(1000, error.destroy)

def addConnection(IP, name, location, leader, VNCPath, addwindow):
    if len(IP) > 0 and len(name) > 0 and len(VNCPath) > 0 and len(location) > 0 and len(leader) > 0:
        connect = sqlite3.connect(resource_path(r'database\dbVNC.db'))
        c = connect.cursor()
        c.execute('INSERT INTO machine (ip, owner, VNC_path) VALUES (?, ?, ?)', (IP, name, VNCPath))
    addwindow.destroy()

def addbutton(password, checkpassword, ui):
    print("Adding a new connnection at " + str(datetime.now()))
    if password == "Fiery.admin":
        checkpassword.destroy()
        addwindow = tk.Toplevel(ui)
        addwindow.config(background='#1C283A')
        addwindow.geometry("1280x720")
        addwindow.overrideredirect(True)
        # set minimum window size value
        addwindow.minsize(1280, 720)
        # set maximum window size value
        addwindow.maxsize(1280, 720)
        addwindow.title("Add a new connection")
        addwindow.iconbitmap("APP.ico")
        title = tk.Message(addwindow, text='Add a new connection VNC', font=('Calibri', 20), fg='#FFFFFF', background='#1C283A', width=360)
        title.place(relx=0.5, rely=0.1, anchor='center')

        img = Image.open(resource_path(r'images\close_button.png'))
        closebuttonimg = ImageTk.PhotoImage(img)
        closebutton = tk.Button(addwindow, image=closebuttonimg, activebackground='#1C283A', background='#1C283A',
                                borderwidth=0, command=lambda: addwindow.destroy())
        closebutton.image=closebuttonimg
        closebutton.place(relx=0.9, rely=0.1)

        IPLabel = tk.Message(addwindow, text='IP', font=('Calibri', 14), fg='#FFFFFF', background='#1C283A', width=40)
        IPEntry = tk.Entry(addwindow, width=30)

        IPLabel.place(relx=0.1, rely=0.3, anchor='center')
        IPEntry.place(relx=0.3, rely=0.3, anchor='center')

        NameLabel = tk.Message(addwindow, text='Company Name', font=('Calibri', 14),  fg='#FFFFFF', background='#1C283A', width=130)
        NameEntry = tk.Entry(addwindow, width=30)

        NameLabel.place(relx=0.14, rely=0.4, anchor='center')
        NameEntry.place(relx=0.3, rely=0.4, anchor='center')

        LocationLabel = tk.Message(addwindow, text= 'Location', font=('Calibri', 14),  fg='#FFFFFF', background='#1C283A', width=70)
        LocationEntry = tk.Entry(addwindow, width=30)

        LocationLabel.place(relx=0.115, rely=0.5, anchor='center')
        LocationEntry.place(relx=0.3, rely=0.5, anchor='center')

        LeaderLabel = tk.Message(addwindow, text='Leader', font=('Calibri', 14), fg='#FFFFFF', background='#1C283A',
                                   width=70)
        LeaderEntry = tk.Entry(addwindow, width=30)

        LeaderLabel.place(relx=0.115, rely=0.6, anchor='center')
        LeaderEntry.place(relx=0.3, rely=0.6, anchor='center')

        VNCLabel = tk.Message(addwindow, text='VNC Path', font=('Calibri', 14),  fg='#FFFFFF', background='#1C283A', width=100)
        VNCEntry = tk.Entry(addwindow, width=50)

        img = Image.open(resource_path(r'images\browse_btn.png'))
        browse_img = ImageTk.PhotoImage(img)
        VNCAdd = tk.Button(addwindow, image=browse_img, bg='#1C283A', borderwidth=0, activebackground='#697589',
                              command=lambda: fileselect(VNCEntry))
        VNCAdd.image = browse_img
        VNCLabel.place(relx=0.12, rely=0.7, anchor='center')
        VNCEntry.place(relx=0.345, rely=0.7, anchor='center')
        VNCAdd.place(relx=0.8, rely=0.7, anchor='center')

        img = Image.open(resource_path(r'images\add_btn.png'))
        add_img = ImageTk.PhotoImage(img)
        addbutton = tk.Button(addwindow, image=add_img, bg='#1C283A', activebackground='#697589', borderwidth=0,
                              command=lambda: addConnection(IPEntry.get(), NameEntry.get(), LocationEntry.get(), LeaderEntry.get(), VNCEntry.get(), addwindow))
        addbutton.image = add_img
        addbutton.place(relx=0.8, rely=0.85, anchor='center')
    else:
        warning = tk.Message(checkpassword, text="Invalid password", font=('Calibri', 14),  fg='#FFFF00', background='#1C283A', width=200)
        warning.place(relx=0.4, rely=0.95)
        warning.after(1000, warning.destroy)

def checkpassword(ui):
    print("Checking access at " + str(datetime.now()))
    checkwindow = tk.Toplevel(ui)
    checkwindow.config(bg='#1C283A')
    checkwindow.geometry('720x480')
    checkwindow.title("Check password")
    checkwindow.iconbitmap("APP.ico")
    checkwindow.overrideredirect(True)

    # set minimum window size value
    checkwindow.minsize(720, 480)
    # set maximum window size value
    checkwindow.maxsize(720, 480)

    img = Image.open(resource_path(r'images\close_button.png'))
    closebuttonimg = ImageTk.PhotoImage(img)
    closebutton = tk.Button(checkwindow, image=closebuttonimg, activebackground='#1C283A', background='#1C283A',
                            borderwidth=0, command=lambda: checkwindow.destroy())
    closebutton.image = closebuttonimg
    closebutton.place(relx=0.9, rely=0.08)

    img = Image.open(resource_path(r'images\check_btn.png'))
    check_img = ImageTk.PhotoImage(img)
    tk.Label(checkwindow, text='Enter your password', bg='#1C283A',font=('Calibri',
                                   20), fg="#FFFFFF").place(relx=0.35, rely=0.2)

    # Create Entry Widget for password
    password = tk.Entry(checkwindow, show="*", width=30)
    password.place(relx=0.38, rely=0.4)

    check_btn = tk.Button(checkwindow, image=check_img, borderwidth=0, bg='#1C283A', fg='#FFFFFF', activebackground='#697589', command=lambda: addbutton(password.get(), checkwindow, ui))
    check_btn.image = check_img
    check_btn.place(relx=0.45, rely=0.6)