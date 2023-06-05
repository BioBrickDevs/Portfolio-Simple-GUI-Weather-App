"""Done by Jari Suomela
    suomela.jari@gmail.com

The goal of this project is to create a weather app that shows the current weather conditions and forecast for a specific location.

This is a working weather app that diplays current weather for searched location. The text box shows details about
the search result for verification that the location is correct. I know it could be formated better but I don't want spend
too much time with this app. I just want to show I'm able to do the tasks required.

Type in location press enter or click search location and then the result box shows information about the location and
the current weather in location is shown and then weather for tomorrow.

You need to use your own Open Weather Api Key to use this program. Since it start to cost if over 1000 requests are made one day
If api key is not updated to real one the app won't display the weather for location.
"""
from geopy.geocoders import Nominatim
import tkinter
from tkinter import ttk
import requests
import json
from PIL import Image, ImageTk
import datetime

OPEN_WEATHER_API_KEY = "Your one call api key here"


def enter_search(evert):
    get_cordinates(input.get())


def change_time():
    now = datetime.datetime.now()
    date_today = now.strftime("%d/%m/%Y")
    time_now = now.strftime("%H:%M:%S")
    # print(f"today: {date_today}")
    # print(f"time: {time_now}")

    datetime_text.config(text=(f"{date_today} {time_now }"))
    count_time()


def count_time():
    window.after(1000, change_time)


def get_weather(lat, lon):
    end_point = "https://api.openweathermap.org/data/3.0/onecall"
    global OPEN_WEATHER_API_KEY
    parameters = {
        "lat": lat,
        "lon": lon,
        "appid": OPEN_WEATHER_API_KEY,
        "exclude": "minutely,hourly",
        "units": "metric"
    }
    response = requests.get(end_point, params=parameters)
    response.raise_for_status()
    weather_data = response.json()
    # with open("file.json", "w") as file:
    #   to_file = json.dumps(weather_data)
    #  file.write(to_file)

    # print(weather_data)

    display_current_weather(weather_data)


def display_current_weather(weather_data):
    temperature = weather_data["current"]["temp"]
    temperature = str(round(temperature)) + " °C"
    # main = weather_data["current"]["weather"][0]["main"]
    description = weather_data["current"]["weather"][0]["description"]
    icon_name = weather_data["current"]["weather"][0]["icon"]

    icon_url = f"http://openweathermap.org/img/wn/{icon_name}@4x.png"
    image_file = requests.get(icon_url)
    with open("current_weather_icon.png", "wb") as file:
        file.write(image_file.content)

    file_name = "./current_weather_icon.png"
    image = Image.open(file_name)
    image = ImageTk.PhotoImage(image)
    label.configure(image=image)
    label.image = image
    text_to_display = f"Current weather {temperature} \n {description}"
    current_weather_text.configure(text=text_to_display)
    display_forecast_tomorrow(weather_data)


def display_forecast_tomorrow(weather_data):
    temperature = weather_data["daily"][0]["temp"]["day"]
    description = weather_data["daily"][0]["weather"][0]["description"]
    temperature = str(round(temperature)) + " °C"

    icon_name = weather_data["daily"][0]["weather"][0]["icon"]

    icon_url = f"http://openweathermap.org/img/wn/{icon_name}@4x.png"
    image_file = requests.get(icon_url)
    with open("tomorrow_weather_icon.png", "wb") as file:
        file.write(image_file.content)

    file_name = "./tomorrow_weather_icon.png"
    image = Image.open(file_name)
    image = ImageTk.PhotoImage(image)
    tomorrow_icon.configure(image=image)
    tomorrow_icon.image = image
    text_to_display = f"Weather tomorrow {temperature} \n {description}"
    tomorrow_weather_text.configure(text=text_to_display)


def get_cordinates(query):
    inputtxt.delete(1.0, tkinter.END)
    geolocator = Nominatim(user_agent="Biobrick Weather App")
    location = geolocator.geocode(query)
    if location:
        inputtxt.insert(tkinter.END, location.address)
        get_weather(location.latitude, location.longitude)


window = tkinter.Tk()

window.title("Weather App by Biobrick")
window.minsize(width=100, height=50)
window.config(padx=10, pady=10, bg="light blue")

input = tkinter.Entry(width=30, bg="light blue")

print(input.get())
input.grid(column=1, row=1)

inputtxt = tkinter.Text(window, height=10,
                        width=25,
                        bg="light blue", )
inputtxt.grid(column=1, row=3)

window.bind('<Return>', enter_search)

button = tkinter.Button(
    text="Search For Location", command=lambda: get_cordinates(input.get()), bg="light blue")
button.grid(column=1, row=2, pady=10)
label = tkinter.Label(bg="light blue")
label.grid(column=1, row=7)

current_weather_text = tkinter.Label(bg="light blue")
current_weather_text.grid(column=1, row=6)
tomorrow_weather_text = tkinter.Label(bg="light blue")
tomorrow_weather_text.grid(column=1, row=8)


now = datetime.datetime.now()
date_today = now.strftime("%d/%m/%Y")
time_now = now.strftime("%H:%M:%S")
datetime_text = tkinter.Label(
    text=(f"{date_today} {time_now }"), bg="light blue")
datetime_text.grid(column=1, row=0, pady=10)

tomorrow_icon = tkinter.Label(bg="light blue")
tomorrow_icon.grid(column=1, row=9)

copyright = tkinter.Label(bg="light blue",
                          text=f"Done by Jari Suomela\n suomela.jari@gmail.com")
copyright.grid(column=1, row=10)
count_time()

window.mainloop()
