import kivy
kivy.require('1.10.0')

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

class WeatherApp(App):

    def __init__(self):
        App.__init__(self)
        self.layout = GridLayout(cols=1)
        self.button_layout = GridLayout(cols=1)
        self.weather_screen = ""
        self.sm = ScreenManager()

    def build(self):


        btn1 = Button(text='1 dzien')
        btn1.bind(on_press=lambda x: self.show_weather('1'))
        self.button_layout.add_widget(btn1)

        btn2 = Button(text='5 dni')
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
        self.weather_screen = Screen(name='W1')
        btn12 = Button(text='5 dni')
        self.weather_screen.add_widget(btn12)
        self.sm.add_widget(self.weather_screen)

        self.sm.current = 'W1'

        print 'show_weather'


if __name__ == '__main__':
    WeatherApp().run()
