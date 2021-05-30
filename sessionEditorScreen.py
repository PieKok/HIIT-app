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
            main_text = str(exo[0]) + ". " + exo[1]
            sec_text = "Work: " + str(exo[2]) + "s / Rest: " + str(exo[3]) + "s"
            items = TwoLineIconListItem(text=main_text, secondary_text=sec_text)
            icon_widget = IconLeftWidget(icon="delete", on_press=self.delete_exo)
            items.add_widget(icon_widget)
            self.ids.exoList.add_widget(items)

    def add_new_exo_button(self):
        app = MDApp.get_running_app()
        app.change_screen('pick_exercise_screen', 'left')

    def add_exo_to_session(self, exo_name, exo_time, rest_time):
        app = MDApp.get_running_app()
        session_str = self.ids.session_name.text

        # Count how many exos are already in the session
        sql_statement1 = "SELECT COUNT(*) FROM " + session_str
        app.cursor.execute(sql_statement1)
        my_old_nb_exos = app.cursor.fetchall()

        # Add the new exo
        my_id = my_old_nb_exos[0][0]+1
        sql_statement2 = "INSERT INTO " + session_str + " VALUES (" + str(my_id) + ",'" + exo_name + "'," + exo_time + "," + rest_time + ");"
        app.cursor.execute(sql_statement2)
        app.connection.commit()

        # Refresh view of all exos
        self.display_saved_session(session_str)

    def delete_exo(self, inst):
        session_str = self.ids.session_name.text
        my_name_exo = inst.parent.parent.children[1].children[2].text
        my_exo_index = my_name_exo.split('.')[0]

        # Delete the item
        app = MDApp.get_running_app()
        sql_statement1 = "DELETE FROM " + session_str + " WHERE id=" + my_exo_index + ";"
        app.cursor.execute(sql_statement1)
        app.connection.commit()

        # Refresh the id of the exos after the one just deleted
        sql_statement2 = "UPDATE " + session_str + " SET id = id - 1 WHERE id > " + my_exo_index + ";"
        app.cursor.execute(sql_statement2)
        app.connection.commit()

        self.display_saved_session(session_str)
