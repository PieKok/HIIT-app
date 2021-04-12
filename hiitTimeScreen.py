from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivymd.app import MDApp


class HIIT_Timer_Screen(Screen):
    str_title = StringProperty()
    str_timer = StringProperty()
    str_round = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.state_round = 0
        self.timer = 999
        self.state_phase = 'prep'
        self.prep_time = 999
        self.work_time = 999
        self.work_time = 999
        self.nb_round = 999

    def start_timer(self, prep_time=5, work_time=45, rest_time=15, nb_round=10):
        self.prep_time = int(prep_time)
        self.work_time = int(work_time)
        self.work_time = int(rest_time)
        self.nb_round = int(nb_round)

        self.init_preparation()

        self.run_timer()
        print(self.timer)

    def init_preparation(self):
        self.state_phase = 'prep'
        self.timer = self.prep_time
        self.state_round = 0
        self.str_title = "Prepare!"
        self.str_timer = str(self.timer)
        self.str_round = str(self.state_round) + "/" + str(self.nb_round)

    def run_timer(self):
        Clock.schedule_interval(self.update, 1)

    def update(self, *kwargs):
        self.timer = self.timer - 1
        self.str_timer = str(self.timer)

    def stop_timer(self):
        Clock.unschedule(self.update)
        app = MDApp.get_running_app()
        app.change_screen('start_HIIT_screen', 'left')




