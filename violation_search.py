import npyscreen

class ViolationSearch(npyscreen.FormBaseNew):
    def create(self):

        self.nextrely += 10
        self.button3 = self.add(npyscreen.ButtonPress, name="Back")
        self.button3.whenPressed = lambda: self.parentApp.switchForm("SEARCHENGINE")

