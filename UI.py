import tkinter as tk
from datetime import datetime

from PIL import Image, ImageTk

from functions import resource_path, readFile, checkpassword, Table

print("Starting ui at " + str(datetime.now()))
ui = tk.Tk()

ui.config(width=1280, height=720, background='#1C283A')
ui.geometry("720x480")
ui.title("VNConnection")
ui.iconbitmap(resource_path("APP.ico"))
ui.overrideredirect(True)

# set minimum window size value
ui.minsize(1280, 720)
# set maximum window size value
ui.maxsize(1280, 720)

# get width & height of screen
width = 1280
height = 720

# set screensize as fullscreen and not resizable
ui.resizable(False, False)

# put image in a label and place label as background
imgTemp = Image.open(resource_path(r'images\plantilla.png'))
img2 = imgTemp.resize((width, height))
img = ImageTk.PhotoImage(img2)
label = tk.Label(ui, image=img)
label.pack()

data = readFile()
print(data)

table = Table(ui, rows=len(data), columns=5, data=data, external_value=ui)
table.place(relx=0.24, rely=0.2)

addbuttonimg = tk.PhotoImage(file=resource_path(r'images\new_client_btn.png'))
addbutton = tk.Button(ui, image=addbuttonimg, bg='#e6e6e6', borderwidth=0, activebackground='#e6e6e6', command=lambda: checkpassword())
addbutton.place(relx=0.125, rely=0.88, anchor='center')

closebuttonimg = tk.PhotoImage(file=resource_path(r'images\close_button.png'))
closebutton = tk.Button(ui, image=closebuttonimg, activebackground='#1C283A', background='#1C283A', borderwidth=0, command=lambda: ui.destroy())
closebutton.place(relx=0.9, rely=0.1)



ui.mainloop()