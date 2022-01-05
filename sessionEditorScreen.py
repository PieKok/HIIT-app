from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.boxlayout import BoxLayout
from functools import partial


class Session_Editor_Screen(Screen):
    editExo_dialog = None

    def clean_screen(self):
        self.ids.session_name.text = ""
        self.ids.exoList.clear_widgets()

    def display_saved_session(self, session_name):
        self.ids.session_name.text = session_name

        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM '" + session_name + "'"
        app.cursor.execute(sql_statement)
        session_exos = app.cursor.fetchall()

        self.display_exos(session_exos)

    def display_exos(self, data_exos):
        # Clear the list if it had been loaded in the past
        self.ids.exoList.clear_widgets()
        for index, exo in enumerate(data_exos):
            main_text = str(exo[0]) + ". " + exo[1]
            sec_text = "Work: " + str(exo[2]) + "s / Rest: " + str(exo[3]) + "s"
            items = TwoLineAvatarIconListItem(text=main_text, secondary_text=sec_text)
            delete_widget = IconLeftWidget(icon="delete", on_press=self.delete_exo)
            edit_widget = IconRightWidget(icon="playlist-edit", on_press=self.open_edit_exo)
            items.add_widget(delete_widget)
            items.add_widget(edit_widget)
            self.ids.exoList.add_widget(items)

    def add_new_exo_button(self):
        app = MDApp.get_running_app()
        app.change_screen('pick_exercise_screen', 'left')

    def add_exo_to_session(self, exo_name, exo_time, rest_time):
        app = MDApp.get_running_app()
        session_str = self.ids.session_name.text

        # Count how many exos are already in the session
        sql_statement1 = "SELECT COUNT(*) FROM '" + session_str + "'"
        app.cursor.execute(sql_statement1)
        my_old_nb_exos = app.cursor.fetchall()

        # Add the new exo
        my_id = my_old_nb_exos[0][0]+1
        sql_statement2 = "INSERT INTO '" + session_str + "' VALUES (" + str(my_id) + ",'" + exo_name + "'," + exo_time + "," + rest_time + ");"
        app.cursor.execute(sql_statement2)
        app.connection.commit()

        # Refresh view of all exos
        self.display_saved_session(session_str)

    def delete_exo(self, inst):
        session_str = self.ids.session_name.text
        my_name_exo = inst.parent.parent.children[2].children[2].text
        my_exo_index = my_name_exo.split('.')[0]

        # Delete the item
        app = MDApp.get_running_app()
        sql_statement1 = "DELETE FROM '" + session_str + "' WHERE id=" + my_exo_index + ";"
        app.cursor.execute(sql_statement1)
        app.connection.commit()

        # Refresh the id of the exos after the one just deleted
        sql_statement2 = "UPDATE '" + session_str + "' SET id = id - 1 WHERE id > " + my_exo_index + ";"
        app.cursor.execute(sql_statement2)
        app.connection.commit()

        self.display_saved_session(session_str)

    def open_edit_exo(self, inst):
        session_str = self.ids.session_name.text
        my_name_exo = inst.parent.parent.children[2].children[2].text
        my_exo_index = my_name_exo.split('.')[0]

        app = MDApp.get_running_app()
        sql_statement = "SELECT * FROM '" + session_str + "' WHERE id=" + my_exo_index + ";"
        app.cursor.execute(sql_statement)
        edited_exo = app.cursor.fetchall()

        self.editExo_dialog = MDDialog(
            type="custom",
            content_cls=EditDialogContent(edited_exo[0]),
            size_hint=(0.8, 0.8),
            buttons=[
                MDFlatButton(
                    text="Cancel", on_release=self.cancel_edit_dialog
                ),
                MDFlatButton(
                    text="Edit", on_release=partial(self.edit_exo, my_exo_index)
                )
            ]
        )
        self.editExo_dialog.open()

    def cancel_edit_dialog(self, inst):
        self.editExo_dialog.dismiss()

    def edit_exo(self, exo_index, inst):
        session_str = self.ids.session_name.text

        new_name = self.editExo_dialog.content_cls.ids.input_name.text
        new_work = self.editExo_dialog.content_cls.ids.input_work.text
        new_rest = self.editExo_dialog.content_cls.ids.input_rest.text

        app = MDApp.get_running_app()
        sql_statement = "UPDATE '" + session_str + "' SET exo = '" + new_name + "', work = '" + new_work + "', rest = '" + new_rest + "' WHERE id=" + exo_index + ";"
        app.cursor.execute(sql_statement)
        app.connection.commit()

        self.editExo_dialog.dismiss()
        self.display_saved_session(session_str)


class EditDialogContent(BoxLayout):
    def __init__(self, edited_exo, **kwargs):
        super().__init__(**kwargs)
        self.ids.input_name.text = edited_exo[1]
        self.ids.input_work.text = str(edited_exo[2])
        self.ids.input_rest.text = str(edited_exo[3])
