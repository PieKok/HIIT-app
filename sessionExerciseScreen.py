from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivymd.app import MDApp
import random


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
    str_equipments = ""
    categories = []
    session_exercises = None

    def create_a_session(self):
        # Read the settings given by the user in the previous screen
        self.get_inputs()

        # Connect to the database and load the exercises
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises"
        app.cursor.execute(sql_statement)
        all_exercises = app.cursor.fetchall()

        filtered_exercises = self.filter_exercises(all_exercises)
        self.session_exercises = self.pick_exercises(filtered_exercises)

        self.display_list_of_exercises(self.session_exercises)

    def get_inputs(self):
        app = MDApp.get_running_app()
        self.prep_time = int(app.root.ids.screen_ss_ID.ids.input_prep_time.text)
        self.work_time = int(app.root.ids.screen_ss_ID.ids.input_work_time.text)
        self.rest_time = int(app.root.ids.screen_ss_ID.ids.input_rest_time.text)
        self.nb_round = int(app.root.ids.screen_ss_ID.ids.input_number_round.text)
        self.nb_warm = int(app.root.ids.screen_ss_ID.ids.input_number_warmup_round.text)
        if app.root.ids.screen_ss_ID.ids.check_jumping.active:
            self.str_equipments = self.str_equipments + "jumping "
        if app.root.ids.screen_ss_ID.ids.check_running.active:
            self.str_equipments = self.str_equipments + "running "
        if app.root.ids.screen_ss_ID.ids.check_mattress.active:
            self.str_equipments = self.str_equipments + "mattress "
        if app.root.ids.screen_ss_ID.ids.check_skipping.active:
            self.str_equipments = self.str_equipments + "skipping "

    def filter_exercises(self, all_ex):
        available_equipments = self.str_equipments.split()

        my_arms_list = list()
        my_cardio_list = list()
        my_core_list = list()
        my_legs_list = list()
        for exo in all_ex:
            ok_equip = True
            required_equipments = exo[2].split()
            for equip_to_be_checked in required_equipments:
                if equip_to_be_checked not in available_equipments:
                    ok_equip = False
            if ok_equip:
                my_exo = list(exo)
                my_exo.append(0)  # Add a counter saying how many times the exo is used
                if exo[1] == "Arms":
                    my_arms_list.append(my_exo)
                elif exo[1] == "Cardio":
                    my_cardio_list.append(my_exo)
                elif exo[1] == "Core":
                    my_core_list.append(my_exo)
                elif exo[1] == "Legs":
                    my_legs_list.append(my_exo)

        filtered_exercises = {"Arms": my_arms_list, "Cardio": my_cardio_list, "Core": my_core_list,
                              "Legs": my_legs_list}

        return filtered_exercises

    def pick_exercises(self, dic_exo):
        picked_exos = list()
        next_category = {"Cardio": "Core", "Core": "Legs", "Legs": "Arms", "Arms": "Cardio"}

        my_cat = "Cardio"
        for i_round in range(1, self.nb_round + 1):
            if i_round > self.nb_warm: # Warm-up is only Cardio exercises
                my_cat = next_category[my_cat]

            my_exo_list = dic_exo[my_cat]
            while not my_exo_list: # In case one category has no exercise
                my_cat = next_category[my_cat]
                my_exo_list = dic_exo[my_cat]
            min_used = min([exo[3] for exo in my_exo_list])  # Use all exercices before reusing a same exercise
            my_selected_exo = random.choice([exo for exo in my_exo_list if exo[3] == min_used])
            picked_exos.append(my_selected_exo)
            my_selected_exo[3] = my_selected_exo[3] + 1

        return picked_exos

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
        app.change_screen('session_screen', 'left')
        app.root.ids.screen_s_ID.start_timer(self.prep_time, self.work_time, self.rest_time, self.nb_round)
