import npyscreen

"""
Plan: 
1. Process input from form into values dictionary {argument:(tuple of arguments?)}
Idea: part of database methods?
2. Create a popup menu to confirm submission at OK
3. If ok, execute input processing
4. Clear fields and restart form.
"""

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
        self.date    = self.add(npyscreen.TitleDateCombo,
                                name='Date:', begin_entry_at=20)
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

        return self.entries  # Check with the others to the dictionary format again

    def prepare_statement(self):
        return """ insert into ticket values(:t_id,
                                             :sin,
                                             :vehicle_no,
                                             :officer_no,
                                             :violation_type,
                                             :t_date,
                                             :place,
                                             :description) """


    def validate_forms(self):
        pass
    
    def on_ok(self):
        # Process information function here
        # Send insert statement here 'insert into ticket values(X,Y,Z)'
        self.validate_forms()

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

