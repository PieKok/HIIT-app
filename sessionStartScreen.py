from kivy.uix.screenmanager import Screen


class SessionStartScreen(Screen):

    def update_round_count(self):
        if self.ids.input_number_warmup_round.text != "":
            my_warm = int(self.ids.input_number_warmup_round.text)
        else:
            my_warm = 0

        if self.ids.input_number_cardio_round.text != "":
            my_cardio = int(self.ids.input_number_cardio_round.text)
        else:
            my_cardio = 0

        if self.ids.input_number_core_round.text != "":
            my_core = int(self.ids.input_number_core_round.text)
        else:
            my_core = 0

        if self.ids.input_number_arms_round.text != "":
            my_arms = int(self.ids.input_number_arms_round.text)
        else:
            my_arms = 0

        if self.ids.input_number_leg_round.text != "":
            my_legs = int(self.ids.input_number_leg_round.text)
        else:
            my_legs = 0

        my_total = my_warm + my_cardio + my_core + my_arms + my_legs
        self.ids.text_nb_round.text = "Total: " + str(my_total) + " rounds"
