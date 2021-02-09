from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('design.kv')


class HIITApp(MDApp):
    def build(self):
        return RootWidget()


class MainScreen(Screen):
    def go_to_exercise_screen(self):
        self.manager.current = "exercise_screen"
    def go_to_session_start_screen(self):
        self.manager.current = "session_start_screen"

class ExerciseScreen(Screen):
    def go_to_home_screen(self):
        self.manager.current = "main_screen"


class SessionStartScreen(Screen):
    def go_to_home_screen(self):
        self.manager.current = "main_screen"


class RootWidget(ScreenManager):
    pass


if __name__ == '__main__':
    print('Will it work like a PyCharm?')
    HIITApp().run()
    print('It worked like a PyCharm!')
