import npyscreen
import cx_Oracle
import os

class AddOwnerOnVehicle(npyscreen.ActionPopup):
    def create(self):
        self.vehicle_id = self.add(npyscreen.TitleText, name='Vehicle ID:', 
                                   begin_entry_at=25, editable=False,
                                   color="STANDOUT")

        # If serial_no was filled in on the NVR form, then use that same serial
        # number. (Otherwise it's easy to forget the value used on the form, and
        # entering a different value defeats the purpose of this popup).
        if self.parentApp.AOOV_default:
            self.vehicle_id.value = self.parentApp.AOOV_default
        self.parentApp.AOOV_default = ''

        self.owner_id = self.add(npyscreen.TitleText, name='Owner ID:',
                                 begin_entry_at=25)

        self.is_primary_owner = self.add(npyscreen.TitleSelectOne, 
                                         name='Primary Owner:',
                                         values=['Y', 'N'], begin_entry_at=25,
                                         scroll_exit=True)

    def validate_forms(self):
        # Ensure SIN is not left blank
        if self.owner_id.value == '':
            npyscreen.notify_confirm("Please enter a SIN.", title="Error",
                                     form_color='STANDOUT', wrap=True,
                                     wide=False, editw=1)
            return False


        # First make sure we don't index into an empty list.
        try:
            is_primary_sel = \
                self.is_primary_owner.values[self.is_primary_owner.value[0]]
        except IndexError:
            npyscreen.notify_confirm("Please specify primary or non-primary.", 
                                     title="Error", form_color='STANDOUT',
                                     wrap=True, wide=False, editw=1)
            return False

        return True 

    def on_ok(self):
        if not self.validate_forms():
            self.editing = True
            return

        # Ensure owner_id references valid sin in db.
        # If not we need to prompt the user to enter the person into the people
        # db. We will open this form as a popup.
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.owner_id.value.\
            ljust(15, ' ')}, query)[0][0] == 0:
            
            # Prompt to add a new person.
            response = npyscreen.notify_ok_cancel(
                "This person does not currently exist.\n"
                "Enter a person with this SIN into the database?", 
                title="Alert", form_color='STANDOUT', 
                wrap=True, editw=1)

            # If user selected ok forward them to the add person form.
            if response:
                self.parentApp.AP_default = self.owner_id.value
                # Set the next form to be the people form. If the add person
                # form exits with switchFormPrevious we should end up back here.
                # self.parentApp.setNextFormPrevious('NEWVEHICLEREGISTRATION')
                self.AP_goto_NVR = True
                self.parentApp.switchForm('ADDPERSON')
            else:
                self.editing=True
                return

        if self.is_primary_owner.value[0] == 0: # 'Y' selected
            self.parentApp.NVR_primary_owner[0] = self.owner_id.value
        elif self.is_primary_owner.value[0] == 1: # 'N' selected
            if self.owner_id.value not in self.parentApp.NVR_other_owners and \
               self.owner_id.value != self.parentApp.NVR_primary_owner[0]:
                self.parentApp.NVR_other_owners.append(self.owner_id.value)

        self.parentApp.switchFormPrevious() 

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
