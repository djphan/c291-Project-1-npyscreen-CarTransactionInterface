import npyscreen

class NewVehicleRegistration(npyscreen.ActionForm):
    def create(self):
        self.serial_no = self.add(npyscreen.TitleText, name='Serial no:')
        self.maker = self.add(npyscreen.TitleText, name='Maker:')
        self.model = self.add(npyscreen.TitleText, name='Model:')
        self.year = self.add(npyscreen.TitleText, name='Year:')
        self.color = self.add(npyscreen.TitleText, name='Color:')
        self.type_id = self.add(npyscreen.TitleText, name='Type id:')
        # self.
        self.button1 = self.add(npyscreen.ButtonPress, name = "Add owner")
        # self.owner = self.add(npyscreen.MultiLineEdit, name=':')

        
    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    
