from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.toolbar import MDToolbar
import exerciseScreen, hiitTimeScreen, sessionStartScreen, sessionScreen
import sqlite3
from kivy.base import EventLoop


class HIITApp(MDApp):
    connection = None
    cursor = None
    dict_back_transitions = {"exercise_screen": "main_screen",
                             "session_start_screen": "main_screen",
                             "start_HIIT_screen": "main_screen",
                             "HIIT_timer_screen": "start_HIIT_screen",
                             "session_screen": "session_start_screen"
                             }

    def on_start(self):
        # Load the exercise database
        self.connection = sqlite3.connect(" exerciseDB.db")
        self.cursor = self.connection.cursor()
        EventLoop.window.bind(on_keyboard=self.return_click)

    def build(self):
        Builder.load_file('main.kv')
        Builder.load_file("sessionstartscreen.kv")
        Builder.load_file("exercisescreen.kv")
        Builder.load_file("starthiitscreen.kv")
        Builder.load_file("hiittimerscreen.kv")
        Builder.load_file("sessionscreen.kv")
        return RootWidget()

    def change_screen(self, name_screen, direction):
        self.root.transition.direction = direction
        self.root.current = name_screen

    def return_click(self, window, key, *args):
        if key == 27:  # escape key or Android return button
            my_current_screen = self.root.current
            my_destination_screen = self.dict_back_transitions[my_current_screen]
            if my_current_screen == "HIIT_timer_screen":
                self.root.ids.screen_ht_ID.abort()
            if my_current_screen == "session_screen":
                self.root.ids.screen_s_ID.abort()
            else:
                self.change_screen(my_destination_screen, "right")
            return True


class MainScreen(Screen):
    pass


class StartHIITScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


class Toolbar(MDToolbar):
    pass


if __name__ == '__main__':
    theApp = HIITApp()
    import bugs

    bugs.fixBugs()
    theApp.run()
