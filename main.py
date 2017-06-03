# -*- coding: utf-8 -*-
import kivy
kivy.require('1.10.0')

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
import urllib2, urllib
import json
from kivy.graphics import *


images_url = "https://www.yahoo.com/sy/os/weather/1.0.1/shadow_icon/60x60/"
baseurl = "https://query.yahooapis.com/v1/public/yql?"
yql_query = "select * from weather.forecast where woeid in" \
            " (select woeid from geo.places(1) where text='torun, pl') and u='c'"


class WeatherApp(App):

    def __init__(self):
        App.__init__(self)
        self.layout = GridLayout(cols=1)
        self.button_layout = GridLayout(cols=1)
        self.weather_screen = ""
        self.sm = ScreenManager()

    def build(self):


        btn1 = Button(text='Aktualna pogoda')
        btn1.bind(on_press=lambda x: self.show_weather('1'))
        self.button_layout.add_widget(btn1)

        btn2 = Button(text='Prognoza na 5 dni')
        btn2.bind(on_press=lambda x: self.show_weather('5'))
        self.button_layout.add_widget(btn2)

        # Create the manager

        weather_screen = Screen(name='Home')
        weather_screen.add_widget(self.button_layout)
        self.sm.add_widget(weather_screen)
        self.sm.current = 'Home'

        self.layout.add_widget(self.sm)

        return self.layout

    def show_weather(self, day):

        yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
        result = urllib2.urlopen(yql_url).read()
        data = json.loads(result)

        weather_layout = GridLayout(cols=1)

        month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul',
                      8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

        days_dict = {'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday', 'Mon': 'Monday',
                     'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday'}

        images_dict = {"Partly Cloudy": "partly_cloudy_day@2x.png",
                       "Scattered Showers": "scattered_showers_day_night@2x.png",
                       "Mostly Cloudy": "mostly_cloudy_day_night@2x.png", "Scattered Thunderstorms": "",
                       "Thunderstorms": "", "Rain": "rain_day_night@2x.png"}

        if day == '1':
            self.weather_screen = Screen(name='W1')

            date_raw = data['query']['results']['channel']['lastBuildDate']
            dates = date_raw.split(', ', 1)[1]

            day = dates.split(' ')[0]
            month = month_dict.keys()[month_dict.values().index(dates.split(' ')[1])]
            year = dates.split(' ')[2]
            hour = dates.split(' ')[3]
            am_pm = dates.split(' ')[4]
            img = images_url + images_dict.values()[images_dict.keys().index(data['query']['results']['channel']['item']['condition']['text'])]
            wimg = AsyncImage(source=img)

            date_time_label = Label(text="{} / {} {} {} {}".format(day, month, year, hour, am_pm))
            day = days_dict.values()[days_dict.keys().index(date_raw.split(', ', 1)[0])]
            day_label = Label(text=day)

            temp = data['query']['results']['channel']['item']['condition']['temp']
            low_temp = data['query']['results']['channel']['item']['forecast'][0]['low']
            high_temp = data['query']['results']['channel']['item']['forecast'][0]['high']

            temp_label = Label(text="Current temperature: "+ temp+u'\N{DEGREE SIGN}'+"C")
            low_temp_label = Label(text="Low temperature: " + low_temp+u'\N{DEGREE SIGN}'+"C")
            high_temp_label = Label(text="High temperature: " + high_temp+u'\N{DEGREE SIGN}'+"C")

            weather_layout.add_widget(date_time_label)
            weather_layout.add_widget(day_label)
            weather_layout.add_widget(wimg)
            weather_layout.add_widget(temp_label)
            weather_layout.add_widget(low_temp_label)
            weather_layout.add_widget(high_temp_label)

            line = Line(points=[100, 100, 200, 100, 100, 200], width=1)

            weather_layout.add_widget(line)
            self.weather_screen.add_widget(weather_layout)
            self.sm.add_widget(self.weather_screen)
            self.sm.current = 'W1'

        else:
            self.weather_screen = Screen(name='W5')

            for _, item in zip(range(5), data['query']['results']['channel']['item']['forecast']):
                date_label = Label(text=item['date'])
                day = days_dict.values()[days_dict.keys().index(item['day'])]
                day_label = Label(text=day)

                low_temp = item['low']
                high_temp = item['high']
                low_temp_label = Label(text="Low temperature: " + low_temp + u'\N{DEGREE SIGN}' + "C")
                high_temp_label = Label(text="High temperature: " + high_temp + u'\N{DEGREE SIGN}' + "C")
                img = images_url + images_dict.values()[
                images_dict.keys().index(item['text'])]
                wimg = AsyncImage(source=img)

                weather_layout.add_widget(date_label)
                weather_layout.add_widget(day_label)
                weather_layout.add_widget(wimg)
                weather_layout.add_widget(low_temp_label)
                weather_layout.add_widget(high_temp_label)


            self.weather_screen.add_widget(weather_layout)
            self.sm.add_widget(self.weather_screen)
            self.sm.current = 'W5'

if __name__ == '__main__':
    WeatherApp().run()
