import npyscreen

class NewVehicleRegistration(npyscreen.ActionForm):
    def create(self):

        self.serial_no = self.add(npyscreen.TitleText, name='Serial No:')
        self.maker = self.add(npyscreen.TitleText, name='Maker:')
        self.model = self.add(npyscreen.TitleText, name='Model:')
        self.year = self.add(npyscreen.TitleText, name='Year:')
        self.color = self.add(npyscreen.TitleText, name='Color:')
        self.type_id = self.add(npyscreen.TitleText, name='Type ID:')
        self.nextrely += 1
        self.button1 = self.add(npyscreen.ButtonPress, name = "Add owner")
        self.button1.whenPressed = self.button_press_add_owner
        self.owner = self.add(npyscreen.MultiLineEdit, name=':')

    def button_press_add_owner(self):
        self.parentApp.switchForm("ADDOWNERONVEHICLE")

    def process_data(self):
        # For year and type_id cast to int if possible
        self.values = {'serial_no': self.serial_no.value,
                       'maker': self.maker.value,
                       'model': self.model.value,
                       'year': '' if self.year.value == '' else int(self.year.value),
                       'color': self.color.value,
                       'type_id' : '' if self.type_id.value == '' else int(self.type_id.value)
                      }

        return self.values

    def prepare_statement(self):
        return """insert into vehicle values (:serial_no,
                                              :maker,
                                              :model,
                                              :year,
                                              :color,
                                              :type_id) """

    def validate_entries(self):
        # check type_id and year separately, but not if they're left
        # blank (to allow NULL values)
        try:
            if not self.year.value == '':
                int(self.year.value)
        except ValueError:
            npyscreen.notify_confirm("Year must be an integer.",
                title="Error", form_color='STANDOUT', wrap=True, 
                wide=False, editw=1)
            return False

        try:
            if not self.type_id.value == '':
                int(self.type_id.value)
        except ValueError:
            npyscreen.notify_confirm("Type ID must be an integer.",
                                     title="Error", form_color='STANDOUT', wrap=True, 
                                     wide=False, editw=1)
            return False

        # check if serial_no is in existing database
        query = "SELECT count(SERIAL_NO) FROM vehicle where SERIAL_NO = :serial_no"
        if self.parentApp.db.query({'serial_no' : self.serial_no.value.ljust(15, ' ')}, query)[0][0]:
            npyscreen.notify_confirm("Serial no already exists in database.", title="Serial no error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        if not self.type_id.value == '':
            query = "SELECT count(type_id) FROM vehicle where type_id = :type_id"
            if self.parentApp.db.query({'type_id' : int(self.type_id.value)}, query)[0][0] == 0:
                npyscreen.notify_confirm("Vehicle Type ID does not exist in database.", title="Type ID Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return False

        return True
 
    def on_ok(self):
        
        if not self.serial_no.value:
            npyscreen.notify_confirm("Please fill in a Serial no.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return        

        if not self.validate_entries():
            self.editing = True
            return

        entry_dict = self.process_data()
        insert = self.prepare_statement()
        error = self.parentApp.db.insert(entry_dict, insert)

        if error:
            # handle error, then return to form.
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)

        self.parentApp.switchForm('NEWVEHICLEREGISTRATION')

    def on_cancel(self):
        self.parentApp.switchForm('MAIN')

