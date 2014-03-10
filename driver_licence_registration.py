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
        self.parentApp.switchFormPrevious()
        
        # attempt to open the image file
        try:
            image_file = open(self.photo.value, 'rb')
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            npyscreen.notify_confirm(error.message, 
                                            editw=1,
                                            title='Image Load failure')

            # change this so it takes you back to filled form on fail
            return

        # if we are succesfull in opening, prep image for db entry
        image = image_file.read()
        self.parentApp.db.cursor.setinputsizes(image=cx_Oracle.BLOB)
        image_file.close() 
        
        # prep and send db statement
        insert = """insert into drive_licence (licence_no, 
                                            sin, class, photo,
                                            issuing_date,
                                            expiring_date)
                                            values (:licence_no,
                                            :class, :photo,
                                            :issuing_date,
                                            :expiring_date)"""
        entry_dict = {'licence_no':self.licence_no, 
                                            'sin':self.sin,
                                            'class':self.licence_class,
                                            'photo':image,
                                            'issuing_date':
                                            self.issuing_date,
                                            'expiring_date':
                                            self.expiring_date}
        self.parentApp.db.cursor.execute(insert, entry_dict) 
                                                
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
