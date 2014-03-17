import npyscreen
import cx_Oracle
import os

class AddOwnerOnVehicle(npyscreen.ActionPopup):
    def create(self):
        self.owner_id = self.add(npyscreen.TitleText, 
                                            name='Owner ID:',
                                            begin_entry_at=25)
        self.vehicle_id = self.add(npyscreen.TitleText, name='Vehicle ID:', 
                                            begin_entry_at=25)
        self.is_primary_owner = self.add(npyscreen.TitleSelectOne, 
                                            name='Primary Owner:',
                                            values=['Y', 'N'],
                                            begin_entry_at=25)
        # if self.parentApp.serial_no:
            # self.vehicle_id.value = self.parentApp.serial_no
         
    def validate_forms(self):
        # ensure sin is not left blank
        if self.owner_id.value == '':
            npyscreen.notify_confirm("Invalid SIN. Person does not exist", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # ensure owner_id references valid sin in db
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.owner_id.value.\
            ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid SIN. Person does not exist", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # check that the vehicle id is in the vehicle table.
        # this requires that the vehicle registration data is entered into the db
        # before owners can be.
        query = "SELECT COUNT(serial_no) FROM vehicle WHERE serial_no = :id"
        if self.parentApp.db.query({'id':self.vehicle_id.value.\
            ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Vehicle ID does not correspond to a registered vehicle", 
                title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # force them to select yes/no for primary owner
        if  not self.is_primary_owner.value:
            npyscreen.notify_confirm("You must indicate if the owner is primary",
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        
        # if they select primary owner, ensure no other primary owner on the vehicle
        # exists in the database, this is just to provide a clear message to the user.
        if self.is_primary_owner.values[self.is_primary_owner.value[0]] == 'Y':
            query = "SELECT count(*) FROM owner where vehicle_id = :v_id \
                and owner_id = :o_id and is_primary_owner = :primary"
            query_dict = {'v_id':self.vehicle_id.value.ljust(15, ' '),
                          'o_id':self.owner_id.value.ljust(15, ' '),
                          'primary':'y'}
            if self.parentApp.db.query(query_dict, query)[0][0] >= 1:
                npyscreen.notify_confirm("This vehicle already has a primary owner registered", 
                title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return False

        return True 

    def on_ok(self):
        # ensure owner_id references valid sin in db
        # if not we need to prompt the user to enter the person
        # into the people db. We will open this form as a popup.
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.owner_id.value.\
            ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid SIN. Person does not exist", 
                title="Error", form_color='STANDOUT', 
                wrap=True, wide=False, editw=1)
            
            # prompt to add a new person.
            response = npyscreen.notify_ok_cancel(\
                "Enter a person with this SIN into the database?", 
                title="Error", form_color='STANDOUT', 
                wrap=True, editw=1)

            # if user selected ok forward them to the 
            # add person form.
            if response:
                # set the next form to be the people form
                # if the add person form exits with switchFormPrevious
                # we should end up back here.
                self.parentApp.setNextForm('ADDPERSON')
            else:
                return
            
            return False

        if not self.validate_forms():
            self.editing = True
            return

        # send data to db
        values = {"owner_id"          :str(self.owner_id.value),
                  "vehicle_id"        :str(self.vehicle_id.value),
                  "is_primary_owner"  :str(self.is_primary_owner.values[self.is_primary_owner.value[0]]).lower()} 
        
        prepare = "INSERT INTO owner VALUES (:owner_id, :vehicle_id, :is_primary_owner)"
        error = self.parentApp.db.insert(values, prepare)
        if error:
            # handle error avoid main menu return
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Error", form_color='STANDOUT', 
                wrap=True, wide=False, editw=1)
            return

        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True,
            wide=False, editw=1)

        # nice to have: append added owners to the vehicle registration form.

        self.parentApp.switchFormPrevious() 

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
