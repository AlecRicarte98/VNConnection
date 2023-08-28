import os
import subprocess
import sys
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog
from ttkthemes.themed_style import ThemedStyle

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def readFile():
    file = open(rf'C:\Users\alecrica\OneDrive - Electronics for Imaging, Inc\000_Services\VNConnection\Clients.txt')
    nameList = []
    for line in file:
        columns = line.split('\t')
        nameList.append(columns[1])
    return nameList

def fileselect(entry):
    file = filedialog.askopenfilename(filetypes=(('Virtual Network Computing files', '*.vnc'), ("All files", "*.*")))
    if file != "":
        entry.insert(0, file)

def connection(connname, ui):
    file = open(rf'C:\Users\alecrica\OneDrive - Electronics for Imaging, Inc\000_Services\VNConnection\Clients.txt')
    vncpath = ''
    for line in file:
        columns = line.split('\t')
        if connname == columns[1]:
            vncpath = columns[2]
            break
    print(vncpath)
    if vncpath != '' and vncpath != 'No_path' and vncpath[-4:] == '.vnc':
        args = r"C:\Program Files (x86)\uvnc bvba\UltraVNC\vncviewer.exe -config " + vncpath
        subprocess.call(args)

    else:
        error = tk.Message(ui, text='Invalid VNC Path', font=('Calibri', 14),  fg='#FFFF00', background='#1C283A', width=200)
        error.place(relx=0.5, rely=0.85, anchor='center')
        error.after(1000, error.destroy)

def addConnection(IP, name, VNCPath, addwindow):
    if len(IP) > 0 and len(name) > 0 and len(VNCPath) > 0:
        with open(rf'C:\Users\alecrica\OneDrive - Electronics for Imaging, Inc\000_Services\VNConnection\Clients.txt', 'a') as f:
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
        addwindow.iconbitmap("EFI_Icono.ico")
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
    checkwindow.iconbitmap("EFI_Icono.ico")


    tk.Label(checkwindow, text="Enter the Password", bg='#1C283A', fg="#FFFFFF", font=('Calibri', 16)).pack(pady=20)

    # Create Entry Widget for password
    password = tk.Entry(checkwindow, show="*", width=30)
    password.pack()

    tk.Button(checkwindow, text="Check", bg='#1C283A', fg='#FFFFFF', activebackground='#697589', font=('Calibri',
                                   14), command=lambda: addbutton(password.get(), checkwindow)).pack(pady=20)

def main():
    print("Starting ui at " + str(datetime.now()))
    ui = tk.Tk()
    style = ThemedStyle(ui)
    style.set_theme("breeze")
    style.configure('Vertical.TScrollbar', background='#2D3C48')
    style.configure("TCombobox", fieldbackground='#2D3C48', background="#2D3C48", foreground='#1C283A',
                    selectbackground='#1975D2')
    ui.option_add("*TCombobox*Listbox*Background", '#2D3C48')
    ui.option_add('*TCombobox*Listbox*Foreground', '#FFFFFF')

    ui.config(width=1280, height=720, background='#1C283A')
    ui.geometry("720x480")
    ui.title("VNConnection")
    ui.iconbitmap(resource_path("EFI_Icono.ico"))



    connmess = tk.Message(ui, text="Connection name: ", font=('Calibri',
                                   16), fg='#FFFFFF', background='#1C283A', width=180)
    connselect = ttk.Combobox(ui, state='readonly', values=readFile(), font=('Calibri',
                                   14), )
    connselect.set('-- Select a Client --')

    connmess.place(relx=0.5, rely=0.2, anchor='center')
    connselect.place(relx=0.5, rely=0.35, anchor='center')

    connbutton = tk.Button(ui, text='Connect', font=('Calibri',
                                   14), bg='#1C283A', fg='#FFFFFF', activebackground='#697589', command=lambda: connection(connselect.get(), ui))
    connbutton.place(relx=0.8, rely=0.6, anchor='center')

    addbutton = tk.Button(ui, text='New Client', bg='#1C283A', font=('Calibri',
                                   14), fg='#FFFFFF', activebackground='#697589', command=lambda: checkpassword())
    addbutton.place(relx=0.2, rely=0.6, anchor='center')


    ui.mainloop()


main()

