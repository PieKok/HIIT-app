from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem
import sqlite3

class HIITApp(MDApp):
    connection = None;
    cursor = None;

    def on_start(self):
        # Load the exercise database
        self.connection = sqlite3.connect(" exerciseDB.db")
        self.cursor = self.connection.cursor()

    def build(self):
        Builder.load_file('design.kv')
        return RootWidget()


class MainScreen(Screen):
    pass


class ExerciseScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.containerList.clear_widgets() # Clear the list if it had been loaded in the past

        # Connect to the database and load the exercises
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises"
        app.cursor.execute(sql_statement)
        exercises = app.cursor.fetchall()
        for ex in exercises:
            items = OneLineListItem(text=ex[0])
            self.ids.containerList.add_widget(items)


class StartHIITScreen(Screen):
    pass


class SessionStartScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


if __name__ == '__main__':
    print('Will it work like a PyCharm?')
    HIITApp().run()
    print('It worked like a PyCharm!')
