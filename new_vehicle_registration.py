import npyscreen

class NewVehicleRegistration(npyscreen.ActionForm):
    def create(self):
        # setup all fields to hold user input, label data, and buttons
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

        self.add(npyscreen.TitleFixedText, name="Primary owner:", 
            editable=False, max_width=16, width=16)
        self.nextrely-=2; self.nextrelx+=20
        self.p_owner = self.add(npyscreen.Pager, height=2, editable=False, 
            max_height=2, width=16, max_width=16)
        self.parentApp.NVR_primary_owner = ['']
        self.p_owner.values = self.parentApp.NVR_primary_owner
        self.nextrely-=1
        self.nextrelx-=20
        self.add(npyscreen.TitleFixedText, name="Other owner(s):", 
            editable=False, max_width=16, width=16, height=1)
        self.nextrely-=2; self.nextrelx+=20
        self.o_owners = self.add(npyscreen.Pager, height=8, editable=False, 
            max_height=8, width=16, max_width=16)
        self.parentApp.NVR_other_owners = []
        self.o_owners.values = self.parentApp.NVR_other_owners
        self.parentApp.NVR_cancelled_entry = None

    # setup button press method to be called when add owner buttons is pressed
    def button_press_add_owner(self):
        # attach attribute to main application for subform accesss
        self.parentApp.AOOV_default = self.serial_no.value
        self.parentApp.switchForm("ADDOWNERONVEHICLE")
    
    # setup process methof to be used to create SQL statement dictionary
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
    
    # run to create the prepare statement
    def prepare_statement(self):
        return """insert into vehicle values (:serial_no,
                                              :maker,
                                              :model,
                                              :year,
                                              :color,
                                              :type_id) """
    
    # this method is run when the user has populated form and 
    # wishes to send the data to the db
    def validate_entries(self):
        # ensure we can convert the user data to the appropriate data types
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
        if self.parentApp.db.query({'serial_no' : self.serial_no.value.ljust(15, ' ')}, 
                query)[0][0]:
            npyscreen.notify_confirm("Serial no already exists in database.", 
                title="Serial no error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        
        # ensure that the provided vehicle type id exists in the database
        if not self.type_id.value == '':
            query = "SELECT count(type_id) FROM vehicle_type where type_id = :type_id"
            if self.parentApp.db.query({'type_id' : int(self.type_id.value)}, 
                query)[0][0] == 0:
                npyscreen.notify_confirm("Vehicle Type ID %s does not exist in database."%self.type_id.value, title="Type ID Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return False

        # notify user that the first owner must be primary
        if self.p_owner.values[0] == '':
            npyscreen.notify_confirm("Please enter a primary owner.", 
                title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        
        # if we pass all of our conditions return true to the caller
        # to indicate it can proceed with database entry
        return True
    
    # method is called when the user presses the ok button on the new vehicle reg form
    def on_ok(self):
        # ensure the user specifies a serial number 
        if not self.serial_no.value:
            npyscreen.notify_confirm("Please fill in a Serial no.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return        

        # call data validation method
        if not self.validate_entries():
            self.editing = True
            return

        # attempt to make the database entry catch any errors that occur
        # and redirect the user back to the form
        entry_dict = self.process_data()
        insert = self.prepare_statement()
        error = self.parentApp.db.insert(entry_dict, insert)
        if error:
            # handle error, then return to form.
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Status", 
                form_color='STANDOUT', wrap=True, wide=False, editw=1)
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
        
        # notify user that entry was successfull
        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', 
            wrap=True, wide=False, editw=1)

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

    # method called when the user selects the cancel button,
    # clears all fields and returns them to the main menu
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

