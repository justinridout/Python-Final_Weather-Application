import tkinter
from datetime import datetime
import time
from tkinter import Label, messagebox

import requests
import zipcodes
from requests.exceptions import HTTPError


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def make_request(zip_c):
    try:

        response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=' + str(
            zip_c) + ',us&APPID=8a8970ef05558bcb0c0598d8b0b610ad')
        api_call = response.json()
        response.raise_for_status()

        return api_call

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6


def make_unix_request(unix_time):
    try:

        response = requests.get('https://showcase.linx.twenty57.net:8081/UnixTime/fromunix?timestamp=' + str(unix_time))
        response.raise_for_status()
        cst_time = datetime_from_utc_to_local(datetime.strptime(response.text, '%Y-%m-%d %H:%M:%S'))

        return cst_time.strftime("%I:%M %p")

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6


def grab_information(call, weather):
    grab_temperatures(call, weather)
    get_condition(call, weather)
    get_humidity(call, weather)
    get_wind(call, weather)
    get_sunrise(call, weather)
    get_sunset(call, weather)


def grab_temperatures(diction, w):
    temperatures = [diction['main']['temp'], diction['main']['temp_min'], diction['main']['temp_max']]
    convert_to_fahrenheit(temperatures, w)


def convert_to_fahrenheit(diction, w):
    count = 0

    for temp in diction:
        if count == 0:
            w.set_temp_now(round((temp - 273.15) * 9 / 5 + 32, 2))
        elif count == 1:
            w.set_low_temp(round((temp - 273.15) * 9 / 5 + 32, 2))
        elif count == 2:
            w.set_high_temp(round((temp - 273.15) * 9 / 5 + 32, 2))

        count = count + 1


def get_condition(diction, w):
    weather = diction['weather'][0]

    w.set_condition(weather['main'])


def get_humidity(call, w):
    w.set_humidity(call['main']['humidity'])


def get_wind(call, w):
    w.set_wind(call['wind']['speed'])


def get_sunrise(call, w):
    w.set_sunrise(make_unix_request(call['sys']['sunrise']))


def get_sunset(call, w):
    w.set_sunset(make_unix_request(call['sys']['sunset']))


def grab_weather(wi, zc):
    call = make_request(zc)

    wi.set_city(call['name'])
    wi.set_state(zipcodes.matching(str(zc))[0]['state'])
    grab_information(call, wi)
    show_weather(wi)


new_buttons = {}
new_cities = {}


def check_zip(wi, zp, mframe, r, btr):
    try:
        if 10000 <= int(zp) <= 99999:
            if zipcodes.is_real(zp):
                wi.set_state(zipcodes.matching(zp)[0]['state'])

                fin = open("user_zip_codes.txt", 'r')
                lines = list(dict.fromkeys(fin.readlines()))
                fin.close()

                f = open("user_zip_codes.txt", "a")
                f.write(zp + "\n")
                f.close()

                found = bool(False)
                for i in range(len(lines)):
                    if lines[i].strip() == zp.strip():
                        found = bool(True)
                        print(found)

                print("OUt of loop bool " + str(found))
                if not found:
                    print("in iff statement")
                    new_cities[zp] = Label(mframe, text=zp).grid(row=r +2, column=1)
                    new_buttons[zp] = tkinter.Button(mframe, text="View", command=lambda t=int(zp): grab_weather(wi, t))
                    new_buttons[zp].grid(row=r + 2, column=2)
                    r += 1
                    btr += 1

                grab_weather(wi, zp)
            else:
                messagebox.showinfo("Zip Code does not exist")
        else:
            messagebox.showinfo("Invalid Zip Code, Must be in ##### format")
    except ValueError:
        messagebox.showinfo("Invalid Zip Code, Must be in ##### format")
    except TypeError:
        messagebox.showinfo("Invalid Zip Code, Must be in ##### format")


def show_weather(wi):

    weather = tkinter.Toplevel()
    weather.title('Weather for ' + wi.city + ', ' + wi.state)
    weather.geometry("250x300")

    city_label = Label(weather, text='Weather for ' + wi.city + ', ' + wi.state)
    city_label.place(x=100, y=10, anchor='center')

    condition_label = Label(weather, text='Condition: ', font='Helvetica 10')
    condition_label.place(x=40, y=30)
    condition_result = Label(weather, text=wi.condition, font='Helvetica 10 bold')
    condition_result.place(x=100, y=30)

    temperature_label = Label(weather, text='Temperature: ', font='Helvetica 10')
    temperature_label.place(x=22, y=50)
    temperature_result = Label(weather, text=str(wi.temp_now) + "°F", font='Helvetica 10 bold')
    temperature_result.place(x=100, y=50)

    temperature_high_label = Label(weather, text='Max Temp: ', font='Helvetica 10')
    temperature_high_label.place(x=32, y=70)
    temperature_high_result = Label(weather, text=str(wi.max_temp) + "°F", font='Helvetica 10 bold')
    temperature_high_result.place(x=100, y=70)

    temperature_low_label = Label(weather, text='Min Temp: ', font='Helvetica 10')
    temperature_low_label.place(x=35, y=90)
    temperature_low_result = Label(weather, text=str(wi.min_temp) + "°F", font='Helvetica 10 bold')
    temperature_low_result.place(x=100, y=90)

    humidity_label = Label(weather, text='Humidity: ', font='Helvetica 10')
    humidity_label.place(x=42, y=110)
    humidity_result = Label(weather, text=wi.humidity, font='Helvetica 10 bold')
    humidity_result.place(x=100, y=110)

    wind_label = Label(weather, text='Wind Speed: ', font='Helvetica 10')
    wind_label.place(x=22, y=130)
    wind_result = Label(weather, text=wi.wind, font='Helvetica 10 bold')
    wind_result.place(x=100, y=130)

    sunrise_label = Label(weather, text='Sunrise: ', font='Helvetica 10')
    sunrise_label.place(x=50, y=150)
    sunrise_result = Label(weather, text=wi.sunrise, font='Helvetica 10 bold')
    sunrise_result.place(x=100, y=150)

    sunset_label = Label(weather, text='Sunset: ', font='Helvetica 10')
    sunset_label.place(x=52, y=170)
    sunset_result = Label(weather, text=wi.sunset, font='Helvetica 10 bold')
    sunset_result.place(x=100, y=170)

    exit_popup = tkinter.Button(weather, text="Close Popup", command=weather.destroy)
    exit_popup.place(x=70, y=190)
