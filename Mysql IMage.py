import mysql.connector
import os
import time
import tkinter as tk
from tkinter import messagebox

path = 'Input'


def print_files():
    # Check If the directory changed...

    namelist = (os.listdir(path))

    cursor.execute("select name from source_images;")
    result = cursor.fetchall()
    sqllist = [x[0]for x in result]

    final = list(set(namelist).symmetric_difference(set(sqllist)))
    print(final)
    for file in final:
        with open(path + "/" + file, 'rb') as fl:
            data = fl.read()
            cursor.execute("insert into source_images values(%s,%s)", (file, data))
            print('Uploading: ' + file)


def watch_for_update():
    # Will print the images paths every 10 seconds(adjustable)
    print_files()
    time.sleep(10)
    con.commit()


# Executing...
try:
    # Insert your data here.
    con = mysql.connector.connect(host="10.0.0.20", user="toor", passwd="fuego8", db="Prn")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Source_images(name text, img LONGBLOB);")
    print('Connected Succesfully')
    while True:
        watch_for_update()


except mysql.connector.Error as err:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "Something went wrong:\n{}".format(err))
    quit()

# Enjoy.


