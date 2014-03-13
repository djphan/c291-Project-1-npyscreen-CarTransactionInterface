import npyscreen
import cx_Oracle
import os 

class DriverLicenceRegistration(npyscreen.ActionForm):
    def create(self):
        self.licence_no = self.add(npyscreen.TitleText, 
                                            color="STANDOUT",
                                            name='Licence no:',
                                            begin_entry_at=20)
        self.nextrely += 1
        self.sin = self.add(npyscreen.TitleText, name='SIN:', 
                                            begin_entry_at=20)
        self.licence_class = self.add(npyscreen.TitleText, 
                                            name='Class:',
                                            begin_entry_at=20)
        self.photo = self.add(npyscreen.TitleFilenameCombo, 
                                            name='Photo:',
                                            begin_entry_at=20)
        self.issuing_date = self.add(npyscreen.TitleDateCombo, 
                                            name='Issuing Date:',
                                            allowClear = True,
                                            begin_entry_at=20)
        self.expiring_date = self.add(npyscreen.TitleDateCombo, 
                                            name='Expiring Date:', 
                                            allowClear=True,
                                            begin_entry_at=20)

        # get a unique licence id number and auto display?
        # more issues because field is varchar
        # query = "SELECT MAX(licence_no) FROM drive_licence"
        # increment max to get unique licence_no
        # self.licence_no.value = self.parentApp.db.query({}, query)[0][0]
        
    def validate_forms(self):
        # if licence no is autogenerated don't check here
        # if this changes, check it.
        query = "SELECT COUNT(licence_no) FROM drive_licence WHERE licence_no = :lic"
        if self.parentApp.db.query({'lic':self.licence_no.value.ljust(15, ' ')}, query)[0][0] != 0:
            npyscreen.notify_confirm("Licence number already in use. Choose another.", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # ensure sin is not left blank
        if self.sin.value == '':
            npyscreen.notify_confirm("Please enter a SIN", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # ensure sin exists in people table
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.sin.value}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid SIN. Person does not exist", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # ensure sin is not already in the drive_licence table
        query = "SELECT COUNT(sin) FROM drive_licence WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.sin.value.ljust(15, ' ')}, query)[0][0] != 0:
            npyscreen.notify_confirm("Person with sin: " + self.sin.value + 
            " is already licenced", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # ensure class is not empty
        if self.licence_class.value == '':
            npyscreen.notify_confirm("Please enter a licence class", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # ensure file path for image is valid
        if not os.path.isfile(self.photo.value):
            npyscreen.notify_confirm("You must select a valid image path", 
                                    title="Bad image path",
                                    form_color='STANDOUT', wrap=True,
                                    wide=False, editw=1)
            return False 

        # check that issue precedes expiry
        if self.issuing_date.value > self.expiring_date.value:
            npyscreen.notify_confirm("Issue date must precede expiry date.", 
            title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        
        return True

    def on_ok(self):
        if not self.validate_forms():
            self.editing = True
            return

        # attempt to open the image file
        try:
            image_file = open(self.photo.value, 'rb')
        except IOError as exc:
            error, = exc.args
            npyscreen.notify_confirm(error.message, 
                                            editw=1,
                                            title='Image Load failure')
            self.editing = True
            return

        # if we are succesfull in opening, prep image for db entry
        image = image_file.read()
        # self.parentApp.db.cursor.setinputsizes(image=cx_Oracle.BLOB)
        image_file.close() 
        
        # prep and send db statement
        insert = """insert into drive_licence (licence_no, 
                                            sin, class, photo,
                                            issuing_date,
                                            expiring_date)
                                            values (:licence_no, :sin,
                                            :class, :photo,
                                            :issuing_date,
                                            :expiring_date)"""
        entry_dict = {'licence_no':str(self.licence_no.value), 
                      'sin':str(self.sin.value),
                      'class':str(self.licence_class.value),
                      'photo':image,
                      'issuing_date':
                          self.issuing_date.value.strftime("%d-%b-%y"),
                      'expiring_date':
                          self.expiring_date.value.strftime("%d-%b-%y")}
        error = self.parentApp.db.insert(entry_dict, insert)
        # error handling
        if error:
            # don't return to main menu
            self.editing = True
            # print error to screen
            npyscreen.notify_confirm(str(error), title="Status", 
                form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return
        self.parentApp.switchFormPrevious()
                                                
    def on_cancel(self):
        self.parentApp.switchForm("MAIN")
