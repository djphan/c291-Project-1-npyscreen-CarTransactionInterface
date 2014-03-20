import npyscreen
import cx_Oracle
import os

class AddOwnerOnVehicle(npyscreen.ActionPopup):
    def create(self):
        self.vehicle_id = self.add(npyscreen.TitleText, name='Vehicle ID:', 
                                   begin_entry_at=25, editable=False,
                                   color="STANDOUT")

        # If serial_no was filled in on the NVR form, then use that same serial number.
        # (otherwise it's easy to forget the value used on the form, and entering a
        # different value defeats the purpose of this popup).
        if self.parentApp.AOOV_default:
            self.vehicle_id.value = self.parentApp.AOOV_default
        self.parentApp.AOOV_default = ''



        self.owner_id = self.add(npyscreen.TitleText, 
                                            name='Owner ID:',
                                            begin_entry_at=25)

        self.is_primary_owner = self.add(npyscreen.TitleSelectOne, 
                                            name='Primary Owner:',
                                            values=['Y', 'N'],
                                            begin_entry_at=25,
                                         scroll_exit=True)
        # if self.parentApp.serial_no:
            # self.vehicle_id.value = self.parentApp.serial_no
         
    def validate_forms(self):
        # ensure sin is not left blank
        if self.owner_id.value == '':
            npyscreen.notify_confirm("Please enter a SIN.", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False


        # Carl: commented out because we check this anyway to see if we should
        # switch to add_person.

        # ensure owner_id references valid sin in db
        # query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        # if self.parentApp.db.query({'sin':self.owner_id.value.\
        #     ljust(15, ' ')}, query)[0][0] == 0:
        #     npyscreen.notify_confirm("Invalid SIN. Person does not exist", 
        #     title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
        #     return False



        # Carl: why are we requiring that the vehicle already be in the db when
        # the point of this form is to add a vehicle to the db?

        # # check that the vehicle id is in the vehicle table.
        # # this requires that the vehicle registration data is entered into the db
        # # before owners can be.
        # query = "SELECT COUNT(serial_no) FROM vehicle WHERE serial_no = :id"
        # if self.parentApp.db.query({'id':self.vehicle_id.value.\
        #     ljust(15, ' ')}, query)[0][0] == 0:
        #     npyscreen.notify_confirm("Vehicle ID does not correspond to a registered vehicle", 
        #         title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
        #     return False

        # I don't think we need to enforce a primary selection
        # only the rules in the test scenarios which are enforced below.
        """
        # Ensure that if no other owners exist the new owner must be reg as primary.
        if  not self.is_primary_owner.value:
            npyscreen.notify_confirm("You must indicate if the owner is primary",
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        """

        # primary check block.
        # first make sure we don't index into an empty list.
        try:
            is_primary_sel = self.is_primary_owner.values[self.is_primary_owner.value[0]]
        except IndexError:
            npyscreen.notify_confirm("Please specify primary or non-primary.", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        
        # # prep query for whether primary owner exists on the vehicle.
        # query = "SELECT count(*) FROM owner where vehicle_id = :v_id \
        #     and is_primary_owner = :primary"

        # query_dict = {'v_id':self.vehicle_id.value.ljust(15, ' '),
        #               'primary':'y'}
        
        # Carl: no need to check these next few, since we aren't going to be
        # registering owners on a vehicle that's already the in database; only
        # on new vehicles. We can just do a single check for primary owner
        # before submitting the whole thing... it's simpler and more user-
        # friendly if they can see the whole transaction at once rather than
        # have to submit 3 or 4 things separately for one transaction.

        # # if primary owner is already registered don't allow them to register a second.
        # if self.parentApp.db.query(query_dict, query)[0][0] >= 1 and is_primary_sel == 'Y':
        #     npyscreen.notify_confirm("This vehicle already has a primary owner registered", 
        #     title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
        #     return False

        # ensure if no primary is registered they are made to be primary.
        # elif self.parentApp.db.query(query_dict, query)[0][0] == 0 \
        #     and is_primary_sel == 'N':
        #     npyscreen.notify_confirm("The first owner must be a primary owner.", 
        #     title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
        #     return False

        return True 

    def on_ok(self):

        if not self.validate_forms():
            self.editing = True
            return

        # ensure owner_id references valid sin in db
        # if not we need to prompt the user to enter the person
        # into the people db. We will open this form as a popup.
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.owner_id.value.\
            ljust(15, ' ')}, query)[0][0] == 0:
            # npyscreen.notify_confirm("Invalid SIN. Person does not exist", 
            #     title="Error", form_color='STANDOUT', 
            #     wrap=True, wide=False, editw=1)
            
            # prompt to add a new person.
            response = npyscreen.notify_ok_cancel(
                "This person does not currently exist.\n"
                "Enter a person with this SIN into the database?", 
                title="Alert", form_color='STANDOUT', 
                wrap=True, editw=1)

            # if user selected ok forward them to the 
            # add person form.
            if response:
                self.parentApp.AP_default = self.owner_id.value
                # set the next form to be the people form. If the add person
                # form exits with switchFormPrevious we should end up back here.
                # self.parentApp.setNextFormPrevious('NEWVEHICLEREGISTRATION')
                self.AP_goto_NVR = True
                self.parentApp.switchForm('ADDPERSON')
            else:
                self.editing=True
                return
            


        # Carl: Instead of adding owner now, just pass owners (whether primary
        # or secondary) back down to new_vehicle_registration, then add them all
        # at once when the user is satisfied with their entire transaction. This
        # will prevent bugs* like being able to add a vehicle with no owners, or
        # being able to add owners to vehicles that already existed in the db.

        #  *or features depending on your perspective, but these would be
        #   outside the specifications.

        # # get the is primary y/n value
        # is_prim = str(self.is_primary_owner.values[self.is_primary_owner.value[0]]).lower()
        # # send data to db
        # values = {"owner_id"          :str(self.owner_id.value),
        #           "vehicle_id"        :str(self.vehicle_id.value),
        #           "is_primary_owner"  :is_prim}
        # prepare = "INSERT INTO owner VALUES (:owner_id, :vehicle_id, :is_primary_owner)"
        # error = self.parentApp.db.insert(values, prepare)
        # if error:
        #     # handle error avoid main menu return
        #     self.editing = True
        #     npyscreen.notify_confirm(str(error), title="Error", form_color='STANDOUT', 
        #         wrap=True, wide=False, editw=1)
        #     return
        # npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True,
        #     wide=False, editw=1)

        # nice to have: append added owners to the vehicle registration form.
        # Carl: Done  :)
        if self.is_primary_owner.value[0] == 0: # 'Y' selected
            self.parentApp.NVR_primary_owner[0] = self.owner_id.value
        elif self.is_primary_owner.value[0] == 1: # 'N' selected
            if self.owner_id.value not in self.parentApp.NVR_other_owners and\
               self.owner_id.value != self.parentApp.NVR_primary_owner[0]:
                self.parentApp.NVR_other_owners.append(self.owner_id.value)


        self.parentApp.switchFormPrevious() 

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
