from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader


class Planned_Session_Screen(Screen):
    str_title = StringProperty()
    str_timer = StringProperty()
    str_round = StringProperty()
    str_exo = StringProperty()
    color_title = ListProperty()
    prep_time = 5

    def __init__(self, **kw):
        super().__init__(**kw)
        self.state_round = 0
        self.timer = 999
        self.state_phase = 'prep'
        self.nb_round = 999
        self.color_title = (255 / 255, 99 / 255, 71 / 255, 255 / 255)
        self.state_running = False
        self.list_exos = None

    def start_timer(self, input_exos):
        self.list_exos = input_exos
        self.nb_round = len(self.list_exos)

        self.init_preparation()

        self.run_timer()

    def init_preparation(self):
        self.state_running = True
        self.state_phase = 'prep'
        self.timer = self.prep_time
        self.state_round = 0
        self.str_title = "Prepare!"
        self.color_title = (50 / 255, 99 / 255, 220 / 255, 255 / 255)
        self.str_timer = str(self.timer)
        self.str_round = str(self.state_round) + "/" + str(self.nb_round)
        self.str_exo = ""

    def run_timer(self):
        Clock.schedule_interval(self.update, 1)

    def stop_timer(self):
        Clock.unschedule(self.update)

    def update(self, *kwargs):
        if self.timer > 0:
            self.timer = self.timer - 1
            self.play_sound()
            self.str_timer = str(self.timer)
        else:
            self.go_to_next_phase()

    def go_to_next_phase(self):
        if self.state_phase == 'prep':
            self.state_round = self.state_round + 1
            self.state_phase = 'work'
            self.timer = self.list_exos[self.state_round-1][2]

            self.str_timer = str(self.timer)
            self.str_title = "Work!"
            self.color_title = (255 / 255, 99 / 255, 71 / 255, 255 / 255)
            self.str_round = str(self.state_round) + "/" + str(self.nb_round)
            self.str_exo = self.list_exos[self.state_round-1][1]

        elif self.state_phase == 'work':
            self.state_phase = 'rest'
            self.timer = self.list_exos[self.state_round-1][3]

            self.str_timer = str(self.timer)
            self.str_title = "Rest"
            self.color_title = (106 / 255, 216 / 255, 139 / 255, 255 / 255)
            if self.state_round < self.nb_round:
                self.str_exo = "Next: " + self.list_exos[self.state_round][1]
            else:
                self.str_exo = ""

        elif self.state_phase == 'rest':
            if self.state_round < self.nb_round:
                self.state_round = self.state_round + 1
                self.state_phase = 'work'
                self.color_title = (255 / 255, 99 / 255, 71 / 255, 255 / 255)
                self.timer = self.list_exos[self.state_round-1][2]

                self.str_timer = str(self.timer)
                self.str_title = "Work!"
                self.str_round = str(self.state_round) + "/" + str(self.nb_round)
                self.str_exo = self.list_exos[self.state_round - 1][1]
            else:
                self.str_title = ""
                self.str_timer = "Over!"
                self.str_round = ""
                self.str_exo = ""
                Clock.unschedule(self.update)

    def play_sound(self):
        if self.timer == 4:
            sound = SoundLoader.load('sounds/3.wav')
            sound.play()
        elif self.timer == 3:
            sound = SoundLoader.load('sounds/2.wav')
            sound.play()
        elif self.timer == 2:
            sound = SoundLoader.load('sounds/1.wav')
            sound.play()
        elif self.timer == 1:
            sound = SoundLoader.load('sounds/DingDing_3secs.wav')
            sound.play()
        else:
            pass

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
        app.change_screen('session_manager_screen', 'right')
