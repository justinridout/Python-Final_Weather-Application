from os import path
from tkinter.ttk import Entry
import functions as f
import tkinter
from tkinter import Label
from classes.weather import Weather


def show_add_zip(wi):

    add_zip = tkinter.Toplevel()
    add_zip.title("Add a new Zip Code")
    info_label = Label(add_zip, text="Please enter City Zip Code")
    info_label.grid(row=0)

    zip_code_label = Label(add_zip, text="Zip Code: ")
    zip_code_label.grid(row=1)
    zip_code_entry = Entry(add_zip)
    zip_code_entry.grid(row=1, column=2)

    submit = tkinter.Button(add_zip, text="Show Weather", width=30, command=lambda: f.check_zip(wi, zip_code_entry.get(), m, rows, buttn_rows))
    submit.grid(row=2)

    exit = tkinter.Button(add_zip, text="Exit", width=30, command=add_zip.destroy)
    exit.grid(row=2, column=2)


if __name__ == '__main__':
    weather_info = Weather()

    m = tkinter.Tk()
    m.title("Choose your city or add new one")
    m.geometry("250x500")

    zips =[]

    if path.exists("user_zip_codes.txt"):
        file = open("user_zip_codes.txt")
        zips = file.readlines()
        file.close()
        zips = list(dict.fromkeys(zips))
        print(zips)

    info_label = Label(m, text="Choose your city or add a new one").grid(row=1, column=1)

    global rows
    rows = 1
    buttn_rows = 2

    for i in range(len(zips)):
        city_label = Label(m, text=zips[i]).grid(row=i + 2, column=1)
        city_button = tkinter.Button(m, text="View", command=lambda t=int(zips[i]): f.grab_weather(weather_info, t))
        city_button.grid(row=i + 2, column=2)
        buttn_rows += 1
        rows += 1

    b = tkinter.Button(m, width= 10, text="Add Zip", command=lambda: show_add_zip(weather_info))
    b.place(relx=.0, rely=1, anchor='sw')
    exit_bttn = tkinter.Button(m, width=10, text="Close", command=m.destroy)
    exit_bttn.place(relx=1.0, rely=1.0, anchor='se')

    m.after(1000, m.update())
    m.mainloop()
