from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock

class HIITApp(MDApp):
    def build(self):
        Builder.load_file('design.kv')
        return RootWidget()


class MainScreen(Screen):
    pass

class ExerciseScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.containerList.clear_widgets()
        for i in range(5):
            items = OneLineListItem(text='Item ' +str(i))
            self.ids.containerList.add_widget(items)


class SessionStartScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


if __name__ == '__main__':
    print('Will it work like a PyCharm?')
    HIITApp().run()
    print('It worked like a PyCharm!')
