from tkinter import *
import requests
from tkinter import messagebox
from geopy.geocoders import Nominatim
API_KEY="##################################"

def get_coor():
    '''Gets Geographic Coordinates based on City name
    Outputs the values to the appropriate Entry widgets'''
    lat_ent.delete(0,END)
    lon_ent.delete(0,END)
    app=Nominatim(user_agent="myApplication")
    location=app.geocode(city_ent.get().title())
    try:
        lat=float(location.raw["lat"])
        lon=float(location.raw["lon"])
    except AttributeError:
        messagebox.showerror(title="Oops",message=f"{city_ent.get().title()} is not a city")
        city_ent.delete(0,END)
    else:
        lat_ent.insert(0,lat)
        lon_ent.insert(0,lon)

def get_forecast():
    '''Gets maximum and minimum temperatures, humidity and wind speed
    After outputting the values it resets the widgets'''
    try:
        lat=float(lat_ent.get())
        lon=float(lon_ent.get())
    except ValueError:
        messagebox.showerror(title="Oops",message="The coordinates you have set are not right. Try again")
    else:
        url=f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        temp_min = float(data["main"]["temp_min"]) - 273.15
        temp_max = float(data["main"]["temp_max"]) - 273.15
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        messagebox.showinfo(title="Today's Forecast",
                                    message=f"Today's Temperature in {city_ent.get().title()} is between {round(temp_min,2)} and {round(temp_max,2)}\n "
                                            f"A wind speed of {round(wind,2)} and humidity of {round(humidity,2)}")
        lon_ent.delete(0,END)
        lat_ent.delete(0,END)
        city_ent.delete(0,END)


window=Tk()
window.title("Weather App")
canvas=Canvas(window,width=320,height=214)
canvas.grid(row=0,column=0,columnspan=3)
bg_pic=PhotoImage(file="weather.png")
bg=canvas.create_image(160,107,image=bg_pic)
city=Label(text="City name:")
city.grid(row=1,column=0)
city_ent=Entry()
city_ent.grid(row=1,column=1)


lat_lbl=Label(text="Latitude: ")
lat_lbl.grid(row=2,column=0)
lat_ent=Entry()
lat_ent.grid(row=2,column=1)
lon_lbl=Label(text="Longitude: ")
lon_lbl.grid(row=3,column=0)
lon_ent=Entry()
lon_ent.grid(row=3,column=1)

coor_but=Button(text="Get Coordinates",command=get_coor)
coor_but.grid(row=1,column=2)

weather_forecast=Button(text="Get Weather Forecast",command=get_forecast)
weather_forecast.grid(row=4,column=1)




window.mainloop()
