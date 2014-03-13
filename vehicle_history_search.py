import npyscreen

class VehicleHistorySearch(npyscreen.FormBaseNew):
    def create(self):

        self.button3 = self.add(npyscreen.ButtonPress, name="Back")
        self.button3.whenPressed = lambda: self.parentApp.switchForm("SEARCHENGINE")
