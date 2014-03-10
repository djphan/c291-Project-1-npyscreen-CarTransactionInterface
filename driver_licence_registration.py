import npyscreen
import cx_Oracle

class DriverLicenceRegistration(npyscreen.ActionForm):
    def create(self):
        self.licence_no = self.add(npyscreen.TitleText, 
                                            name='Licence no:')
        self.sin = self.add(npyscreen.TitleText, name='SIN:')
        self.licence_class = self.add(npyscreen.TitleText, 
                                            name='Class:')
        self.photo = self.add(npyscreen.TitleFilenameCombo, 
                                            name='Photo:')
        self.issuing_date = self.add(npyscreen.TitleDateCombo, 
                                            name='Issuing Date:',
                                            allowClear = True)
        self.expiring_date = self.add(npyscreen.TitleDateCombo, 
                                            name='Expiring Date:', 
                                            allowClear=True)

    def on_ok(self):
        # call db method on provided data

        
        # attempt to open the image file
        try:
            image_file = open(self.photo.value, 'rb')
        except IOError as exc:
            error, = exc.args
            npyscreen.notify_confirm(error.message, 
                                            editw=1,
                                            title='Image Load failure')

            # change this so it takes you back to filled form on fail
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
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return
        self.parentApp.switchFormPrevious()
                                                
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
