from hiitTimeScreen import HIIT_Timer_Screen
from kivy.clock import Clock
from kivymd.app import MDApp


class Session_Screen(HIIT_Timer_Screen):
    def abort(self):
        Clock.unschedule(self.update)
        app = MDApp.get_running_app()
        app.change_screen('session_start_screen', 'right')
