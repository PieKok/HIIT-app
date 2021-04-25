from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu


def attribute_image_file(category):
    images_files_switcher = {
        "Arms": "images/icon-arm.jpg",
        "Cardio": "images/icon-cardio.png",
        "Core": "images/icons-core.jpg",
        "Legs": "images/icons-legs.jpg"
    }
    return images_files_switcher.get(category, "images/question_mark.jpg")


class ExerciseScreen(Screen):
    add_ex_dialog = None

    def on_pre_enter(self, *args):
        self.display_all_exercises()

    def display_all_exercises(self):
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

    def display_searched_exercises(self, search_text):
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises WHERE name LIKE '%" + search_text + "%'"
        app.cursor.execute(sql_statement)
        exercises = app.cursor.fetchall()
        self.display_list_of_exercises(exercises)

    def button_add_exercise(self):
        if not self.add_ex_dialog:
            self.add_ex_dialog = MDDialog(
                title="Add exercise",
                type="custom",
                content_cls=AddExerciseDialogContent(),
                size_hint=(0.8, 0.8),
                buttons=[
                    MDFlatButton(
                        text="Cancel", on_release=self.cancel_add
                    ),
                    MDFlatButton(
                        text="OK", on_release=self.add_ex
                    )
                ]
            )
        # self.add_ex_dialog.set_normal_height()
        self.add_ex_dialog.open()

    def cancel_add(self, inst):
        self.add_ex_dialog.dismiss()
        print('Cancel')

    def add_ex(self, inst):
        my_name = self.add_ex_dialog.content_cls.ids.field_name.text
        my_category = self.add_ex_dialog.content_cls.ids.dropdown_item.current_item
        if my_category != '' and my_name != '' and self.check_name_ex(my_name):
            print(my_name)
            print(my_category)
            self.add_ex_dialog.dismiss()
        else:
            pass

    def check_name_ex(self, my_name):
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises WHERE name='" + my_name.capitalize() + "'"
        app.cursor.execute(sql_statement)
        is_present = app.cursor.fetchall()
        return not is_present

class AddExerciseDialogContent(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu_items = [
            {"text": "Cardio"},
            {"text": "Legs"},
            {"text": "Arms"},
            {"text": "Core"}]
        self.menu = MDDropdownMenu(
            caller=self.ids.dropdown_item,
            items=menu_items,
            position="center",
            width_mult=4,
            callback=self.set_item
        )

    def set_item(self, instance_menu_item):
        self.ids.dropdown_item.set_item(instance_menu_item.text)
        self.menu.dismiss()
