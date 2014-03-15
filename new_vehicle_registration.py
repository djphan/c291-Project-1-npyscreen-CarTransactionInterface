import npyscreen

class NewVehicleRegistration(npyscreen.ActionForm):
    def create(self):
        self.serial_no = self.add(npyscreen.TitleText, name='Serial no:')
        self.maker = self.add(npyscreen.TitleText, name='Maker:')
        self.model = self.add(npyscreen.TitleText, name='Model:')
        self.year = self.add(npyscreen.TitleText, name='Year:')
        self.color = self.add(npyscreen.TitleText, name='Color:')
        self.type_id = self.add(npyscreen.TitleText, name='Type id:')
        self.nextrely += 1
        self.button1 = self.add(npyscreen.ButtonPress, name = "Add owner")
        self.button1.whenPressed = self.button_press_add_owner
        # self.owner = self.add(npyscreen.MultiLineEdit, name=':')
        # self.parentApp.serial_no = None

    def button_press_add_owner(self):
        # check if serial has been filled so we can
        # auto fill it in the subform
        # if self.serial_no.value:
            # self.parentApp.serial_no = self.serial_no.value
        
        self.parentApp.switchForm("ADDOWNERONVEHICLE")

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

