from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.toolbar import MDToolbar
import exerciseScreen
import sqlite3


class HIITApp(MDApp):
    connection = None
    cursor = None

    def on_start(self):
        # Load the exercise database
        self.connection = sqlite3.connect(" exerciseDB.db")
        self.cursor = self.connection.cursor()

    def build(self):
        Builder.load_file('design.kv')
        return RootWidget()

    def change_screen(self,name_screen,direction):
        self.root.transition.direction = direction
        self.root.current = name_screen


class MainScreen(Screen):
    pass


class StartHIITScreen(Screen):
    def back_to_home_screen(self):
        self.root.ids.manager.direction = "left"
        self.root.ids.manager.current = "home"


class SessionStartScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


class Toolbar(MDToolbar):
    pass


if __name__ == '__main__':
    print('Will it work like a PyCharm?')
    HIITApp().run()
    print('It worked like a PyCharm!')
