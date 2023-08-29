import sqlite3
from functions import resource_path

connect = sqlite3.connect(resource_path('database\dbVNC.db'))
c = connect.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY,
              Name TEXT,
              Country TEXT,
              Leader TEXT,
              UNIQUE (Name)
              )''')

c.execute('''CREATE TABLE IF NOT EXISTS machine(id INTEGER PRIMARY KEY,
                 IP TEXT
                 Owner TEXT,
                 VNC_path TEXT,
                 UNIQUE(IP)
                 )''')