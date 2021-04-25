from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
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
    ex_dialog = None

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
            items = OneLineAvatarListItem(text=ex[0], on_release=self.open_exercise)
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
        self.add_ex_dialog.open()

    def cancel_add(self, inst):
        self.add_ex_dialog.dismiss()

    def add_ex(self, inst):
        my_name = self.add_ex_dialog.content_cls.ids.field_name.text.capitalize()
        my_category = self.add_ex_dialog.content_cls.ids.dropdown_item.current_item
        if my_category != '' and my_name != '' and self.check_name_ex(my_name):
            str_equipment = ""
            if self.add_ex_dialog.content_cls.ids.check_jumping.active:
                str_equipment = str_equipment + "jumping / "
            if self.add_ex_dialog.content_cls.ids.check_running.active:
                str_equipment = str_equipment + "running / "
            if self.add_ex_dialog.content_cls.ids.check_mattress.active:
                str_equipment = str_equipment + "mattress / "
            if self.add_ex_dialog.content_cls.ids.check_skip.active:
                str_equipment = str_equipment + "skipping rope"

            app = MDApp.get_running_app()
            app.cursor.execute("INSERT INTO exercises (name, category, equipment) VALUES (?, ?, ?);",
                               [my_name, my_category, str_equipment])
            app.connection.commit()

            self.display_all_exercises()
            self.add_ex_dialog.dismiss()
        else:
            pass

    def check_name_ex(self, my_name):
        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises WHERE name='" + my_name + "'"
        app.cursor.execute(sql_statement)
        is_present = app.cursor.fetchall()
        return not is_present

    def open_exercise(self, inst):
        print(inst.text)

        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM exercises WHERE name='" + inst.text + "'"
        app.cursor.execute(sql_statement)
        my_exercise = app.cursor.fetchall()

        self.ex_dialog = MDDialog(
            type="custom",
            content_cls=ExerciseDialogContent(ex=my_exercise),
            size_hint=(0.8, 0.8),
            buttons=[
                MDFlatButton(
                    text="Cancel", on_release=self.cancel_ex_dialog
                ),
                MDFlatButton(
                    text="Delete", on_release=self.delete_ex
                )
            ]
        )
        self.ex_dialog.open()

    def cancel_ex_dialog(self, inst):
        self.ex_dialog.dismiss()

    def delete_ex(self, inst):
        my_ex_name = self.ex_dialog.content_cls.ids.field_name.text
        app = MDApp.get_running_app()
        app.cursor.execute("DELETE FROM exercises WHERE name='" + my_ex_name + "'")
        app.connection.commit()

        self.display_all_exercises()
        self.ex_dialog.dismiss()


class ExerciseDialogContent(BoxLayout):
    def __init__(self, ex, **kwargs):
        super().__init__(**kwargs)

        self.ids.field_name.text = ex[0][0]
        self.ids.field_category.text = ex[0][1]

        if "jumping" in ex[0][2]:
            self.ids.check_jumping.active = True
        if "running" in ex[0][2]:
            self.ids.check_running.active = True
        if "mattress" in ex[0][2]:
            self.ids.check_mattress.active = True
        if "skipping rope" in ex[0][2]:
            self.ids.check_skip.active = True


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
