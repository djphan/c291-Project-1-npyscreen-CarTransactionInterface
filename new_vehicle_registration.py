import npyscreen

class NewVehicleRegistration(npyscreen.ActionForm):
    def create(self):

        self.nextrelx+=1
        self.serial_no = self.add(npyscreen.TitleText, name='Serial No:')
        self.maker = self.add(npyscreen.TitleText, name='Maker:')
        self.model = self.add(npyscreen.TitleText, name='Model:')
        self.year = self.add(npyscreen.TitleText, name='Year:')
        self.color = self.add(npyscreen.TitleText, name='Color:')
        self.type_id = self.add(npyscreen.TitleText, name='Type ID:')
        self.nextrely += 1; self.nextrelx-=2
        self.button1 = self.add(npyscreen.ButtonPress, name = "Add owner")
        self.button1.whenPressed = self.button_press_add_owner
        self.nextrelx+=2

        self.add(npyscreen.TitleFixedText, name="Primary owner:", editable=False, max_width=16, width=16)
        self.nextrely-=2; self.nextrelx+=20
        self.p_owner = self.add(npyscreen.Pager, height=2, editable=False, max_height=2, width=16, max_width=16)
        self.parentApp.NVR_primary_owner = ['']
        self.p_owner.values = self.parentApp.NVR_primary_owner
        self.nextrely-=1
        self.nextrelx-=20
        self.add(npyscreen.TitleFixedText, name="Other owner(s):", editable=False, max_width=16, width=16, height=1)
        self.nextrely-=2; self.nextrelx+=20
        self.o_owners = self.add(npyscreen.Pager, height=8, editable=False, max_height=8, width=16, max_width=16)
        self.parentApp.NVR_other_owners = []
        self.o_owners.values = self.parentApp.NVR_other_owners
        self.parentApp.NVR_cancelled_entry = None

    def button_press_add_owner(self):
        self.parentApp.AOOV_default = self.serial_no.value
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
                npyscreen.notify_confirm("Vehicle Type ID %s does not exist in database."%self.type_id.value, title="Type ID Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return False

        if self.p_owner.values[0] == '':
            npyscreen.notify_confirm("Please enter a primary owner.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
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

        # send primary owner data to db
        values = {"owner_id"          :self.p_owner.values[0],
                  "vehicle_id"        :self.serial_no.value,
                  "is_primary_owner"  :'y'}
        prepare = "INSERT INTO owner VALUES (:owner_id, :vehicle_id, :is_primary_owner)"
        error = self.parentApp.db.insert(values, prepare)
        if error:
            # handle error avoid main menu return
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Error", form_color='STANDOUT', 
                wrap=True, wide=False, editw=1)
            return


        # send each secondary owner data to db
        for owner in self.o_owners.values:
            values = {"owner_id"          :owner,
                      "vehicle_id"        :self.serial_no.value,
                      "is_primary_owner"  :'n'}
            prepare = "INSERT INTO owner VALUES (:owner_id, :vehicle_id, :is_primary_owner)"
            error = self.parentApp.db.insert(values, prepare)
            if error:
                # handle error avoid main menu return
                self.editing = True
                npyscreen.notify_confirm(str(error), title="Error", form_color='STANDOUT', 
                    wrap=True, wide=False, editw=1)
                return
            
        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)

        self.serial_no.value = ''
        self.maker.value = ''
        self.model.value = ''
        self.year.value = ''
        self.color.value = ''
        self.type_id.value = ''
        self.parentApp.NVR_primary_owner = ['']
        self.parentApp.NVR_other_owners = []
        self.o_owners.values = self.parentApp.NVR_other_owners
        self.p_owner.values = self.parentApp.NVR_primary_owner



    def on_cancel(self):
        self.serial_no.value = ''
        self.maker.value = ''
        self.model.value = ''
        self.year.value = ''
        self.color.value = ''
        self.type_id.value = ''
        self.parentApp.NVR_primary_owner = ['']
        self.parentApp.NVR_other_owners = []
        self.o_owners.values = self.parentApp.NVR_other_owners
        self.p_owner.values = self.parentApp.NVR_primary_owner

        self.parentApp.switchForm('MAIN')

