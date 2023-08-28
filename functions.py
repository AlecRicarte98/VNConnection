import os
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from tkinter import filedialog



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

def addConnection(IP, name, VNCPath, addwindow):
    if len(IP) > 0 and len(name) > 0 and len(VNCPath) > 0:
        with open(resource_path('Clients.txt'), 'a') as f:
            f.write(f"\n{IP}\t{name}\t{VNCPath}")
    addwindow.destroy()

def addbutton(password, checkpassword):
    print("Adding a new connnection at " + str(datetime.now()))
    if password == "Fiery.admin":
        checkpassword.destroy()
        addwindow = tk.Tk()
        addwindow.config(background='#1C283A')
        addwindow.geometry("720x480")
        addwindow.title("Add a new connection")
        addwindow.iconbitmap("APP.ico")
        title = tk.Message(addwindow, text='Add a new connection VNC', font=('Calibri', 16), fg='#FFFFFF', background='#1C283A', width=360)
        title.place(relx=0.5, rely=0.1, anchor='center')

        IPLabel = tk.Message(addwindow, text='IP', font=('Calibri', 14), fg='#FFFFFF', background='#1C283A', width=40)
        IPEntry = tk.Entry(addwindow, width=30)

        IPLabel.place(relx=0.1, rely=0.25, anchor='center')
        IPEntry.place(relx=0.3, rely=0.25, anchor='center')

        NameLabel = tk.Message(addwindow, text='Name', font=('Calibri', 14),  fg='#FFFFFF', background='#1C283A', width=50)
        NameEntry = tk.Entry(addwindow, width=30)

        NameLabel.place(relx=0.1, rely=0.45, anchor='center')
        NameEntry.place(relx=0.3, rely=0.45, anchor='center')

        VNCLabel = tk.Message(addwindow, text='VNC Path', font=('Calibri', 14),  fg='#FFFFFF', background='#1C283A', width=50)
        VNCEntry = tk.Entry(addwindow, width=50)
        VNCAdd = tk.Button(addwindow, text='...', bg='#1C283A', fg='#FFFFFF', activebackground='#697589', font=('Calibri', 14),
                              command=lambda: fileselect(VNCEntry))

        VNCLabel.place(relx=0.1, rely=0.65, anchor='center')
        VNCEntry.place(relx=0.38, rely=0.65, anchor='center')
        VNCAdd.place(relx=0.8, rely=0.65, anchor='center')

        addbutton = tk.Button(addwindow, text='Add', bg='#1C283A', fg='#FFFFFF', activebackground='#697589', font=('Calibri', 14),
                              command=lambda: addConnection(IPEntry.get(), NameEntry.get(), VNCEntry.get(), addwindow))
        addbutton.place(relx=0.8, rely=0.85, anchor='center')
    else:
        warning = tk.Message(checkpassword, text="Invalid password", font=('Calibri', 14),  fg='#FFFF00', background='#1C283A', width=200)
        warning.pack()
        warning.after(1000, warning.destroy)

def checkpassword():
    print("Checking access at " + str(datetime.now()))
    checkwindow = tk.Tk()
    checkwindow.config(bg='#1C283A')
    checkwindow.geometry('360x300')
    checkwindow.title("Check password")
    checkwindow.iconbitmap("APP.ico")


    tk.Label(checkwindow, text="Enter the Password", bg='#1C283A', fg="#FFFFFF", font=('Calibri', 16)).pack(pady=20)

    # Create Entry Widget for password
    password = tk.Entry(checkwindow, show="*", width=30)
    password.pack()

    tk.Button(checkwindow, text="Check", bg='#1C283A', fg='#FFFFFF', activebackground='#697589', font=('Calibri',
                                   14), command=lambda: addbutton(password.get(), checkwindow)).pack(pady=20)