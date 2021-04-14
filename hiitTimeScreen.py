from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivymd.app import MDApp


class HIIT_Timer_Screen(Screen):
    str_title = StringProperty()
    str_timer = StringProperty()
    str_round = StringProperty()
    color_title = ListProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.state_round = 0
        self.timer = 999
        self.state_phase = 'prep'
        self.prep_time = 999
        self.work_time = 999
        self.rest_time = 999
        self.nb_round = 999
        self.color_title = (255/255, 99/255, 71/255, 255/255)
        self.state_running = False

    def start_timer(self, prep_time=5, work_time=45, rest_time=15, nb_round=10):
        self.prep_time = int(prep_time)
        self.work_time = int(work_time)
        self.rest_time = int(rest_time)
        self.nb_round = int(nb_round)

        self.init_preparation()

        self.run_timer()
        print(self.timer)

    def init_preparation(self):
        self.state_running = True
        self.state_phase = 'prep'
        self.timer = self.prep_time
        self.state_round = 0
        self.str_title = "Prepare!"
        self.color_title = (50 / 255, 99 / 255, 220 / 255, 255 / 255)
        self.str_timer = str(self.timer)
        self.str_round = str(self.state_round) + "/" + str(self.nb_round)

    def run_timer(self):
        Clock.schedule_interval(self.update, 1)

    def stop_timer(self):
        Clock.unschedule(self.update)

    def update(self, *kwargs):
        if self.timer > 0:
            self.timer = self.timer - 1
            self.str_timer = str(self.timer)
        else:
            self.go_to_next_phase()

    def go_to_next_phase(self):
        if self.state_phase == 'prep':
            self.state_round = self.state_round + 1
            self.state_phase = 'work'
            self.timer = self.work_time

            self.str_timer = str(self.timer)
            self.str_title = "Work!"
            self.color_title = (255 / 255, 99 / 255, 71 / 255, 255 / 255)
            self.str_round = str(self.state_round) + "/" + str(self.nb_round)

        elif self.state_phase == 'work':
            self.state_phase = 'rest'
            self.timer = self.rest_time

            self.str_timer = str(self.timer)
            self.str_title = "Rest"
            self.color_title = (106 / 255, 216 / 255, 139 / 255, 255 / 255)

        elif self.state_phase == 'rest':
            if self.state_round < self.nb_round:
                self.state_round = self.state_round + 1
                self.state_phase = 'work'
                self.color_title = (255 / 255, 99 / 255, 71 / 255, 255 / 255)
                self.timer = self.work_time

                self.str_timer = str(self.timer)
                self.str_title = "Work!"
                self.str_round = str(self.state_round) + "/" + str(self.nb_round)
            else:
                self.str_title = " "
                self.str_timer = "Over!"
                self.str_round = " "
                Clock.unschedule(self.update)

    def toggle(self):
        if self.state_running:
            self.state_running = False
            self.stop_timer()
        else:
            if self.str_timer != "Over!":
                self.state_running = True
                self.run_timer()

    def abort(self):
        Clock.unschedule(self.update)
        app = MDApp.get_running_app()
        app.change_screen('start_HIIT_screen', 'left')
