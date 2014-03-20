import npyscreen
import datetime
import cx_Oracle
import os

class DriverLicenceRegistration(npyscreen.ActionForm):
    """
    Record information necessary to issue a driver licence.

    Required information:
      Licence no
      SIN (will prompt to add new person if SIN is not already in database)
    Optional information:
      Photo
      Issuing Date
      Expiring Date

    Also links explicitly to the Add Person form via the "Add new person"
    button.
    """
    def create(self):
        self.nextrelx += 1
        self.licence_no = self.add(npyscreen.TitleText, name='Licence no:',
                                   begin_entry_at=20)
        self.nextrely += 1
        self.sin = self.add(npyscreen.TitleText, name='SIN:', begin_entry_at=20)

        self.licence_class = self.add(npyscreen.TitleText, name='Class:',
                                      begin_entry_at=20)

        self.photo = self.add(npyscreen.TitleFilenameCombo, name='Photo:',
                              begin_entry_at=20)

        self.issuing_date = self.add(npyscreen.TitleDateCombo,
                                     name='Issuing Date:', allowClear=True,
                                     begin_entry_at=20)

        self.expiring_date = self.add(npyscreen.TitleDateCombo,
                                      name='Expiring Date:', allowClear=True,
                                      begin_entry_at=20)

        self.nextrely+=1; self.nextrelx-=2
        self.button1 = self.add(npyscreen.ButtonPress, name="Add new person")
        self.button1.whenPressed = self.button_press_add_person
        self.nextrelx+=2

    def button_press_add_person(self):
        self.parentApp.switchForm("ADDPERSON")

    def validate_forms(self):
        query = """SELECT COUNT(licence_no) FROM drive_licence WHERE
                   licence_no = :lic"""
        if self.parentApp.db.query({'lic':self.licence_no.value.ljust(15, ' ')},
            query)[0][0] != 0:
            npyscreen.notify_confirm(
                "Licence number already in use. Choose another.", title="Error",
                form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # Ensure sin is not left blank
        if self.sin.value == '':
            npyscreen.notify_confirm(
                "Please enter a SIN", title="Error", form_color='STANDOUT',
                wrap=True, wide=False, editw=1)
            return False

        # Ensure sin exists in people table
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query(
            {'sin':self.sin.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm(
                "Invalid SIN. Person does not exist", title="Error",
                form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # Ensure sin is not already in the drive_licence table
        query = "SELECT COUNT(sin) FROM drive_licence WHERE sin = :sin"
        if self.parentApp.db.query(
            {'sin':self.sin.value.ljust(15, ' ')}, query)[0][0] != 0:
            npyscreen.notify_confirm(
                "Person with sin: " + self.sin.value + " is already licenced",
                title="Error", form_color='STANDOUT', wrap=True, wide=False,
                editw=1)
            return False

        # Ensure file path for image is valid
        if self.photo.value:
            if not os.path.isfile(self.photo.value):
                npyscreen.notify_confirm(
                    "You must select a valid image path",
                    title="Bad image path", form_color='STANDOUT', wrap=True,
                    wide=False, editw=1)
                return False

        # Make sure we don't try to date format an empty string.
        if self.issuing_date.value:
            self.issuing_date.value = \
                self.issuing_date.value.strftime("%d-%b-%y")
        if self.expiring_date.value:
            self.expiring_date.value = \
                self.expiring_date.value.strftime("%d-%b-%y")

        return True

    def on_ok(self):

        # Deal with sin entered not being in db. If not we need to prompt the
        # user to enter the person into the people table. We will open this form
        # as a popup.
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query(
            {'sin':self.sin.value.ljust(15, ' ')}, query)[0][0] == 0:
            # prompt to add a new person.
            response = npyscreen.notify_ok_cancel(
                "This person does not exist.\n"
                "Enter a person with this SIN into the database?",
                title="Alert", form_color='STANDOUT',
                wrap=True, editw=1)

            # If user selected ok forward them to the add person form.
            if response:
                # Set the next form to be the people form. If the add person
                # form exits with switchFormPrevious we should end up back here.
                self.parentApp.setNextForm('ADDPERSON')
            else:
                return
            return False

        # validate the form.
        if not self.validate_forms():
            self.editing = True
            return

        # attempt to open the image file
        if self.photo.value:
            try:
                image_file = open(self.photo.value, 'rb')
            except IOError as exc:
                error, = exc.args
                npyscreen.notify_confirm(error.message, editw=1,
                                         title='Image Load failure')
                self.editing = True
                return

        # If we are successful in opening, prep image for db entry.
        if self.photo.value:
            image = image_file.read()
        self.parentApp.db.cursor.setinputsizes(photo=cx_Oracle.BLOB)
        if self.photo.value:
            image_file.close()
        else: # Should be null value.
            image = ''

        # prep and send db statement
        insert = """INSERT INTO drive_licence (licence_no, sin, class, photo,
                    issuing_date, expiring_date) VALUES (:licence_no, :sin,
                    :class, :photo, :issuing_date, :expiring_date)"""

        entry_dict = {'licence_no':str(self.licence_no.value),
                      'sin':str(self.sin.value),
                      'class':str(self.licence_class.value),
                      'photo':image,
                      'issuing_date':self.issuing_date.value,
                      'expiring_date':self.expiring_date.value}

        error = self.parentApp.db.insert(entry_dict, insert)
        if error:
            self.editing = True # don't return to main menu
            # print error to screen
            npyscreen.notify_confirm(str(error), title="Status",
                                     form_color='STANDOUT', wrap=True,
                                     wide=False, editw=1)
            return

        # If we get here we have a successful entry. Notify the user.
        npyscreen.notify_confirm("Success!", title="Status",
                                 form_color='STANDOUT', wrap=True,
                                 wide=False, editw=1)

        # Clear the form for the next entry
        self.licence_no.value = ''
        self.sin.value = ''
        self.licence_class.value = ''
        self.photo.value = ''
        self.issuing_date.value = ''
        self.expiring_date.value = ''
        self.parentApp.switchFormPrevious() # exit

    def on_cancel(self):
        # Just clear the form and exit back to main menu.
        self.licence_no.value = ''
        self.sin.value = ''
        self.licence_class.value = ''
        self.photo.value = ''
        self.issuing_date.value = ''
        self.expiring_date.value = ''
        self.parentApp.switchForm("MAIN")
