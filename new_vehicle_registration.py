import npyscreen

class NewVehicleRegistration(npyscreen.ActionForm):
    def create(self):
        self.serial_no = self.add(npyscreen.TitleText, name='Serial no:')
        self.maker = self.add(npyscreen.TitleText, name='Maker:')
        self.model = self.add(npyscreen.TitleText, name='Model:')
        self.year = self.add(npyscreen.TitleText, name='Year:')
        self.color = self.add(npyscreen.TitleText, name='Color:')
        self.type_id = self.add(npyscreen.TitleText, name='Type ID:')
        # self.
        self.button1 = self.add(npyscreen.ButtonPress, name = "Add owner")
        # self.owner = self.add(npyscreen.MultiLineEdit, name=':')

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
        # Check if serial_no is in existing database
        query = "SELECT count(SERIAL_NO) FROM vehicle where SERIAL_NO = :serial_no"
        if self.parentApp.db.query({'serial_no' : self.serial_no.value.ljust(15, ' ')}, query)[0][0]:
            npyscreen.notify_confirm("Serial no already exists in database.", title="Serial no error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # Check if type_id entered as a string, if so return error
        try: 
            if self.type_id.value != '':
                int(self.type_id.value)

        except ValueError:
            npyscreen.notify_confirm("Vehicle type ID not a valid number.", title="type_id Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # Check if type_id is in existing database
        # Dan Note: Does not work right now. Registers all type_ids as invalid. Check query???
        query = "SELECT count(type_id) FROM vehicle_type where type_id = :type_id"
        if self.parentApp.db.query({'type_id' : int(self.type_id.value)}, query)[0][0] == 0:
            npyscreen.notify_confirm("Vehicle Type ID does not exist in database.", title="Type id error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        return True
 
    def on_ok(self):
        try:
            # are all the forms filled?
            assert all([self.serial_no.value])
            # can price be converted to a float (with optional '$') ?
            if self.year.value != '':
                int(self.year.value)

        except AssertionError:
            npyscreen.notify_confirm("Please fill in a Serial no. Field left blank", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return        

        except ValueError:
            npyscreen.notify_confirm("Year is not a valid number.", title="Year Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return 

        if not self.validate_entries():
            self.editing = True
            npyscreen.notify_confirm("Yes", title="Year Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        entry_dict = self.process_data()
        insert = self.prepare_statement()
        error = self.parentApp.db.insert(entry_dict, insert)

        if error:
            # handle error
            # don't return to main menu
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)

        self.parentApp.switchForm('NEWVEHICLEREGISTRATION')

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    
