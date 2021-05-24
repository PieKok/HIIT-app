from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu


def attribute_image_file(category):
    images_files_switcher = {
        "Arms": "images/icon-arm.jpg",
        "Cardio": "images/icon-cardio.png",
        "Core": "images/icons-core.jpg",
        "Legs": "images/icons-legs.jpg"
    }
    return images_files_switcher.get(category, "images/question_mark.jpg")


class Pick_Exercise_Screen(Screen):
    menu_category = None
    searched_category = None
    searched_text = None

    def on_pre_enter(self, *args):
        self.ids.exo_name.text = ""
        self.ids.input_work.text = "45"
        self.ids.input_rest.text = "15"
        self.ids.dropdown_category.text = "All"
        self.ids.dropdown_category.current_item = "All"
        self.ids.dropdown_category.ids.label_item.text = "All"
        self.ids.search_field.text = ""
        self.searched_category = None
        self.searched_text = None

        menu_items = [
            {"text": "Cardio"},
            {"text": "Legs"},
            {"text": "Arms"},
            {"text": "Core"},
            {"text": "All"}]
        self.menu_category = MDDropdownMenu(
            caller=self.ids.dropdown_category,
            items=menu_items,
            position="bottom",
            width_mult=3,
            callback=self.filter_category)

        self.display_searched_exercises()

    def display_searched_exercises(self):
        is_cat_searched = not ((not self.searched_category) or (self.searched_category == "All"))
        is_text_searched = not ((not self.searched_text) or (self.searched_text == ""))
        if not is_cat_searched and not is_text_searched:
            sql_statement = "SELECT * FROM exercises"
        elif not is_cat_searched and is_text_searched:
            sql_statement = "SELECT * FROM exercises WHERE name LIKE '%" + self.searched_text + "%'"
        elif is_cat_searched and not is_text_searched:
            sql_statement = "SELECT * FROM exercises WHERE category = '" + self.searched_category + "'"
        else:
            sql_statement = "SELECT * FROM exercises WHERE name LIKE '%" + self.searched_text + "%' AND category = '" + self.searched_category + "'"

        app = MDApp.get_running_app()
        app.cursor.execute(sql_statement)
        exercises = app.cursor.fetchall()
        self.display_list_of_exercises(exercises)

    def display_list_of_exercises(self, exercises):
        # Clear the list if it had been loaded in the past
        self.ids.containerList.clear_widgets()
        for ex in exercises:
            items = OneLineAvatarListItem(text=ex[0], on_release=self.select_exo)
            image_path = attribute_image_file(ex[1])
            image_widget = ImageLeftWidget(source=image_path)
            items.add_widget(image_widget)
            self.ids.containerList.add_widget(items)

    def filter_category(self, instance_menu_item):
        self.ids.dropdown_category.set_item(instance_menu_item.text)
        self.searched_category = instance_menu_item.text
        self.display_searched_exercises()
        self.menu_category.dismiss()

    def filter_text(self, search_text):
        self.searched_text = search_text
        self.display_searched_exercises()

    def select_exo(self, inst):
        self.ids.exo_name.text = inst.text
