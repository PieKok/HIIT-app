from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineIconListItem, IconLeftWidget

class Session_Editor_Screen(Screen):
    def clean_screen(self):
        self.ids.session_name.text = ""
        self.ids.exoList.clear_widgets()

    def display_saved_session(self, session_name):
        self.ids.session_name.text = session_name

        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM " + session_name
        app.cursor.execute(sql_statement)
        session_exos = app.cursor.fetchall()

        self.display_exos(session_exos)

    def display_exos(self, data_exos):
        # Clear the list if it had been loaded in the past
        self.ids.exoList.clear_widgets()
        for index, exo in enumerate(data_exos):
            main_text = str(index+1) + ". " + exo[0]
            sec_text = "Work: " + str(exo[1]) + "s / Rest: " + str(exo[2]) + "s"
            items = TwoLineIconListItem(text=main_text, secondary_text = sec_text)
            icon_widget = IconLeftWidget(icon="delete", on_press=self.delete_exo)
            items.add_widget(icon_widget)
            self.ids.exoList.add_widget(items)

    def add_new_exo_button(self):
        app = MDApp.get_running_app()
        app.change_screen('pick_exercise_screen', 'left')

    def delete_exo(self, inst):
        pass
