from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, IconRightWidget
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton


class Session_Manager_Screen(Screen):
    session_dialog = None

    def on_pre_enter(self, *args):
        self.display_all_sessions()

    def display_all_sessions(self):
        # Connect to the database and load the exercises
        app = MDApp.get_running_app()
        sql_statement = "SELECT name FROM sqlite_master WHERE type='table';"
        app.cursor.execute(sql_statement)
        sessions_names = app.cursor.fetchall()
        sessions_names.remove(('exercises',))

        self.ids.sessionList.clear_widgets()
        for session in sessions_names:
            item = OneLineAvatarIconListItem(text=session[0], on_release=self.dialog_session)
            icon_widget = IconRightWidget(icon="run", on_press=self.start_session)
            item.add_widget(icon_widget)
            self.ids.sessionList.add_widget(item)

    def dialog_session(self, inst):
        self.session_dialog = MDDialog(
            type="custom",
            content_cls=SessionDialogContent(inst.text),
            size_hint=(0.8, 0.8),
            buttons=[
                MDFlatButton(
                    text="Cancel", on_release=self.cancel_session_dialog
                ),
                MDFlatButton(
                    text="Edit", on_release=self.edit_session
                )
            ]
        )
        self.session_dialog.open()

    def cancel_session_dialog(self, inst):
        self.session_dialog.dismiss()

    def edit_session(self, inst):
        self.session_dialog.dismiss()
        my_session_name = self.session_dialog.content_cls.ids.session_name.text
        app = MDApp.get_running_app()
        app.change_screen('session_editor_screen', 'left')
        app.root.ids.screen_sed_ID.display_saved_session(my_session_name)

    def create_session(self):
        app = MDApp.get_running_app()
        app.change_screen('session_editor_screen', 'left')

    def start_session(self, inst):
        pass


class SessionDialogContent(BoxLayout):
    def __init__(self, session_name, **kwargs):
        super().__init__(**kwargs)
        self.ids.session_name.text = session_name

    def delete_session(self, session_name):
        app = MDApp.get_running_app()
        print("delete action")
        app.cursor.execute("DROP TABLE " + session_name)
        app.connection.commit()
        app.root.ids.screen_sm_ID.session_dialog.dismiss()
        app.root.ids.screen_sm_ID.display_all_sessions()
