from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
import sqlite3


def attribute_image_file(category):
    images_files_switcher = {
        "Arms": "images/icon-arm.jpg",
        "Cardio": "images/icon-cardio.png",
        "Core": "images/icons-core.jpg",
        "Legs": "images/icons-legs.jpg"
    }
    return images_files_switcher.get(category, "images/question_mark.jpg")


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


class MainScreen(Screen):
    pass


class ExerciseScreen(Screen):
    def on_pre_enter(self, *args):
        # Connect to the database and load the exercises
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises"
        app.cursor.execute(sql_statement)
        exercises = app.cursor.fetchall()
        self.display_list_of_exercises(exercises)

    def display_list_of_exercises(self, exercises):
        # Clear the list if it had been loaded in the past
        self.ids.containerList.clear_widgets()
        for ex in exercises:
            items = OneLineAvatarListItem(text=ex[0])
            image_path = attribute_image_file(ex[1])
            image_widget = ImageLeftWidget(source=image_path)
            items.add_widget(image_widget)
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
