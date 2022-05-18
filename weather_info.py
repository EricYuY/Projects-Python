import requests
from pprint import pprint
from tkinter import *
from tkinter import ttk

API_Key= '8acacf11b2eaceb4d40300ced0d793c2'
metric='metric'
weather={"temperatura":"","Humedad":""}

def get_weather():
    weather_data=requests.get(base_url).json()
    #pprint(weather_data)
    temperatura=weather_data["main"]["temp"]
    humedad=weather_data["main"]["humidity"]
    weather["temperatura"]=temperatura
    weather["Humedad"]=humedad
    #pprint('Temperatura actual en {} es: {}'.format(city,temperatura))

def display_city_name(root):
    city_label = Label(root, text=f"{city}")
    city_label.config(font=("Consolas", 28))
    city_label.pack(side='top')

def display_stats(root):
    temp = Label(root, text=f"Temperature: {weather['temperatura']} °C")
    humidity = Label(root, text=f"Humidity: {weather['Humedad']} %")

    temp.config(font=("Consolas", 22))
    humidity.config(font=("Consolas", 16))

    temp.pack(side='top')
    humidity.pack(side='top')

def main():
    global city, base_url

    city=input("Enter a city:")
    #city ="Lima"

    base_url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_Key}&units={metric}"

    get_weather()
    #print(weather["temperatura"])
    
    root = Tk()
    root.geometry("450x150")
    root.title("Weather App - {}".format(city))
    display_city_name(root)
    display_stats(root)
    root.mainloop()

if __name__ == "__main__":
    main()
