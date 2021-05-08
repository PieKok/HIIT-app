from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivymd.app import MDApp

def attribute_image_file(category):
    images_files_switcher = {
        "Arms": "images/icon-arm.jpg",
        "Cardio": "images/icon-cardio.png",
        "Core": "images/icons-core.jpg",
        "Legs": "images/icons-legs.jpg"
    }
    return images_files_switcher.get(category, "images/question_mark.jpg")

class Session_Exercise_Screen(Screen):
    prep_time = 0
    work_time = 0
    rest_time = 0
    nb_round = 0
    nb_warm = 0

    def create_a_session(self, prep_time=5, work_time=45, rest_time=15, nb_round=10, nb_warm=5):
        self.prep_time = prep_time
        self.work_time = work_time
        self.rest_time = rest_time
        self.nb_round = nb_round
        self.nb_warm = nb_warm

        # Connect to the database and load the exercises
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises"
        app.cursor.execute(sql_statement)
        all_exercises = app.cursor.fetchall()
        self.display_list_of_exercises(all_exercises)

    def display_list_of_exercises(self, exercises):
        # Clear the list if it had been loaded in the past
        self.ids.exerciseList.clear_widgets()
        for ex in exercises:
            items = OneLineAvatarListItem(text=ex[0])
            image_path = attribute_image_file(ex[1])
            image_widget = ImageLeftWidget(source=image_path)
            items.add_widget(image_widget)
            self.ids.exerciseList.add_widget(items)

    def start_session(self):
        app = MDApp.get_running_app()
        app.change_screen('session_screen','left')
        app.root.ids.screen_s_ID.start_timer(self.prep_time,self.work_time,self.rest_time,self.nb_round)