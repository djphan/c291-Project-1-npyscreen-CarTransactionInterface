import npyscreen
import cx_Oracle
import datetime
import os
import pdb

class AddPerson(npyscreen.ActionPopup):
    def create(self):
        self.sin = self.add(npyscreen.TitleText, name='SIN')

        # (Carl) - Added ability for AddPerson to take a default SIN:
        #   For example, this form is accessed by Auto Transaction when the user
        #   enters a buyer not in the database. Auto Transaction will pass this
        #   new SIN to parentApp.AP_default for use here. If no value is passed,
        #   then self.sin will still be editable.
        if self.parentApp.AP_default is not None:
            self.sin.value = self.parentApp.AP_default
            self.parentApp.AP_default = None
            self.sin.editable = False
            self.sin.color = "STANDOUT"
            
        self.name = self.add(npyscreen.TitleText, name='Name')
        self.height = self.add(npyscreen.TitleText, name='Height') 
        self.weight = self.add(npyscreen.TitleText, name='Weight') 
        self.eye_color = self.add(npyscreen.TitleText, name='Eye color') 
        self.hair_color = self.add(npyscreen.TitleText, name='Hair color') 
        self.addr = self.add(npyscreen.TitleText, name='Address') 
        self.birthday = self.add(npyscreen.TitleDateCombo, name='Birthday',
                                        allowClear=True) 
        self.gender = self.add(npyscreen.TitleSelectOne, name='Gender',
                                            values=['M', 'F'], scroll_exit=True)
    
    def validate_forms(self):
        # ensure sin is not left blank
        if self.sin.value == '':
            npyscreen.notify_confirm("Invalid SIN. Person does not exist", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # ensure sin is not already in the people table
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.sin.value.ljust(15, ' ')}, 
            query)[0][0] != 0:
            npyscreen.notify_confirm("A person already exists with the given SIN.", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # check that the name can be cast to a string
        if self.name.value:
            try:
                if len(str(self.name.value)) > 40:
                    npyscreen.notify_confirm("Person name must be less than\
                    40 chars.", title="Error", form_color='STANDOUT', 
                    wrap=True, wide=False, editw=1)
            except exception as error:
                npyscreen.notify_confirm("A person already exists with the given SIN.", 
                title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return False

        # if user entered a height ensure we van convert to float.
        if self.height.value:
            # deal with float for weight
            try:
                # if user provides a height
                # try to convert height to float
                # if we get an error notify
                float(self.height.value)
            except ValueError:
                npyscreen.notify_confirm("Height must be a number.", title="Error", 
                    form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return False
      
        # if user entered a weight ensure we van convert to float.
        if self.weight.value: 
            # deal with float for weight.
            try:
                # if user provides a weight
                # try to convert weight to float
                # if we get an error notify
                float(self.weight.value)
            except ValueError:
                npyscreen.notify_confirm("Weight must be a number.", title="Error", 
                    form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return False
        
        if not self.birthday.value:
            self.birthday.value = datetime.date.today()

        if self.gender.value:
            # if a gender is specified format it for entry
            self.gender_choice = self.gender.get_selected_objects()[0].lower()
        else:
            # if no value is given, show an error.
            npyscreen.notify_confirm("You must indicate gender.",
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # if everything checks out return true.
        return True 

    def on_ok(self):
        if not self.validate_forms():
            self.editing = True
            return

        # format and send data to db
        entry_dict = {"sin"       :str(self.sin.value),
                  "name"          :str(self.name.value),
                  "height"        :self.height.value,
                  "weight"        :self.weight.value,
                  "eyecolor"      :str(self.eye_color.value),
                  "haircolor"     :str(self.hair_color.value),
                  "addr"          :str(self.addr.value),
                  "gender"        :self.gender_choice,
                  "birthday"      :self.birthday.value.strftime("%d-%b-%y") # formatted for oracle
                      }
                   

        insert = """
            INSERT INTO people (sin, name, height, weight, eyecolor, haircolor, addr,
            gender, birthday) values (:sin, :name, :height, :weight, :eyecolor,
            :haircolor, :addr, :gender, :birthday)
            """


        error = self.parentApp.db.insert(entry_dict, insert)
        if error:
            # handle error avoid main menu return
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Error", 
                form_color='STANDOUT', 
                wrap=True, wide=False, editw=1)
            return

        npyscreen.notify_confirm("Success!", title="Status", 
            form_color='STANDOUT', wrap=True,
            wide=False, editw=1)
        
        # teleport us to the form from which we came!
        self.parentApp.switchFormPrevious() 

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
