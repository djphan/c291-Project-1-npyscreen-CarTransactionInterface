import npyscreen
import datetime

class ViolationRecord(npyscreen.ActionForm):

    def create(self):
        self.t_id    = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                                name="Ticket ID:", begin_entry_at=20,
                                editable=False, color="STANDOUT")
        self.nextrely += 1

        self.sin = self.add(npyscreen.TitleText, name='Violator SIN:',begin_entry_at=20)
        self.vehicle_no = self.add(npyscreen.TitleText, name='Vehicle Serial:', begin_entry_at=20)
        self.officer_no = self.add(npyscreen.TitleText, name='Officer ID:', begin_entry_at=20)
        self.violation_type = self.add(npyscreen.TitleText, name='Violation Type:', begin_entry_at=20)
        self.date    = self.add(npyscreen.TitleDateCombo, name='Date:', begin_entry_at=20)
        self.place = self.add(npyscreen.TitleText, name='Place:',begin_entry_at=20)
        self.nextrely+=1
        self.d_title    = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                                name="Description:", begin_entry_at=20,
                                editable=False, color="STANDOUT")
        self.description = self.add(npyscreen.MultiLineEdit, name='Description:', relx=22, rely=11)        

        # get maximum current ticket_id
        query = "SELECT MAX(ticket_no) FROM ticket"
        # set t_id to one greater
        self.t_id.value = str(1 + self.parentApp.db.query({}, query)[0][0])


    def process_information(self):
        self.entries = {'t_id' : self.t_id.value,
                        'sin' : self.sin.value,
                        'vehicle_no' : self.vehicle_no.value,
                        'officer_no' : self.officer_no.value,
                        'violation_type': self.violation_type.value,
                        "t_date" :self.date.value.strftime("%d-%b-%y"), # formatted for oracle
                        'place' : self.place.value,
                        'description' : self.description.value
                        }
        return self.entries
        
    def prepare_statement(self):
        return """insert into ticket values(:t_id, :sin, :vehicle_no,
                                            :officer_no, :violation_type,
                                            :t_date, :place, :description) """

    def validate_forms(self):
        # validate Violator SIN:
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.sin.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid Violator SIN.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # validate Vehicle Serial:
        query = "SELECT COUNT(serial_no) FROM vehicle WHERE serial_no = :ser"
        if self.parentApp.db.query({'ser':self.vehicle_no.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid vehicle serial number.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # validate Officer ID (SIN):
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.officer_no.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid Officer ID.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # validate Violation Type:
        query = "SELECT COUNT(vtype) FROM ticket_type WHERE vtype = :v_type"
        if self.parentApp.db.query({'v_type':self.violation_type.value.ljust(10, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid Violation Type.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        return True
    
    def on_ok(self):
        # Process information function here

        
        if not self.validate_forms():
            self.editing = True
            return

        if self.date.value == '': # set date to today if unspecified
            self.date.value = datetime.date.today()

        entry_dict = self.process_information()
        insert = self.prepare_statement()
        error = self.parentApp.db.insert(entry_dict, insert)
        if error:
            # handle error
            # don't return to main menu
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)

        self.parentApp.switchForm("VIOLATIONRECORD")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

