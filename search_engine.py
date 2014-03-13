import npyscreen

class SearchEngine(npyscreen.FormBaseNew):
    def create(self):
        self.button0 = self.add(npyscreen.ButtonPress, name="Driver Search")
        self.button0.whenPressed = lambda: self.parentApp.switchForm("DRIVER_SEARCH")
        self.button1 = self.add(npyscreen.ButtonPress, name="Violation Search")
        self.button1.whenPressed = lambda: self.parentApp.switchForm("VIOLATION_SEARCH")
        self.button2 = self.add(npyscreen.ButtonPress, name="Vehicle History Search")
        self.button2.whenPressed = lambda: self.parentApp.switchForm("VEHICLE_HISTORY_SEARCH")
        self.nextrely += 16
        self.nextrelx += 65
        self.button3 = self.add(npyscreen.ButtonPress, name="Back")
        self.button3.whenPressed = lambda: self.parentApp.switchForm("MAIN")
