import npyscreen
import cx_Oracle
import os
import pdb

class AddPerson(npyscreen.ActionForm):
    def create(self):
        self.sin = self.add(npyscreen.TitleText, name='SIN')
        self.name = self.add(npyscreen.TitleText, name='Name')
        self.height = self.add(npyscreen.TitleText, name='Height') 
        self.weight = self.add(npyscreen.TitleText, name='Weight') 
        self.eye_color = self.add(npyscreen.TitleText, name='Eye color') 
        self.hair_color = self.add(npyscreen.TitleText, name='Hair color') 
        self.addr = self.add(npyscreen.TitleText, name='Address') 
        self.birthday = self.add(npyscreen.TitleDateCombo, name='Birthday',
                                        allowClear=True) 
        self.gender = self.add(npyscreen.TitleSelectOne, name='Gender',
                                            values=['M', 'F'])
    
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
        
        # if user makes a selection format the value else set it to empty string.
        if self.gender.value:
            # if a gender is specified format it for entry
            self.gender.value = str(self.gender.values[self.gender.value[0]]).lower(), 
            npyscreen.notify_confirm("You must indicate gender.",
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        else:

            # if no value is given avoid indexing into the gendervalues list
            self.gender.value = ''

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
                  "gender"        :self.gender.value,
                  "birthday"      :self.birthday.value}
                   

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
        
        # stick the sin onto the parent app so we can access it the 
        # the form we return to.
        self.parentApp.sinForAddOwner = self.sin.value

        # teleport us to the form from which we came!
        self.parentApp.switchFormPrevious() 

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
