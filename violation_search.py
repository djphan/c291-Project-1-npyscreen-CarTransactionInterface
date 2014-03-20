import npyscreen

class ViolationSearch(npyscreen.ActionFormCarl):
    def create(self):
        self.chooser = self.add(npyscreen.SelectOne, max_height=2,
                                scroll_exit=True)
        self.chooser.values = ["Search by SIN", 
            "Search by licence number"]
        self.nextrely+=1
        # NOTE: When an entry is selected, the value of self.chooser.value will
        # be a list containing the index of the entry in the above list - in
        # this example, [0] or [1]. If nothing is selected, self.chooser.value
        # will be [].

        self.user_query = self.add(npyscreen.TitleText, name="Search Query:",
                                   begin_entry_at=15, use_two_lines=False, 
                                   field_width=54)
        self.nextrely-=1   
        self.query_confirm = self.add(npyscreen.ButtonPress, name="OK", relx=70,
                                    scroll_exit = True)
        self.query_confirm.whenPressed = self.process_query

        self.results = self.add(npyscreen.Pager, name="Results:", height=16,
                                max_height=16, scroll_exit=True,
                                slow_scroll=True, exit_left=True, exit_right=True)
        
    def on_ok(self):
        self.parentApp.switchForm("SEARCHENGINE")        

    def process_query(self):
        # ensure user has selected search type
        if not self.chooser.value:
            npyscreen.notify_confirm("Please select a search type.", editw=1, title='Error')
            return
        
        if not self.user_query.value:
            npyscreen.notify_confirm("Please enter a SIN or licence number.", 
                editw=1, title='Error')
            return
    
        # build query for when user picks "Search by sin"
        if self.chooser.value[0] == 0:
            query = """
                SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype,
                    t.vdate, t.place, t.descriptions, tt.fine
                FROM ticket t, ticket_type tt
                WHERE tt.vtype (+)= t.vtype
                      AND UPPER(t.violator_no) = UPPER(:violator_no)
            """
            results = self.parentApp.db.query({"violator_no":self.user_query.
                value.ljust(15, ' ')}, query)
        
        # build query for when user selects "Search by licence number"
        elif self.chooser.value[0] == 1:
            query = """
                SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no, t.vtype,
                    t.vdate, t.place, t.descriptions, tt.fine
                FROM ticket t, ticket_type tt, drive_licence d
                WHERE tt.vtype (+)= t.vtype
                      AND UPPER(d.licence_no) = UPPER(:licence_no)
                      AND d.sin (+)= t.violator_no
            """
            results = self.parentApp.db.query({"licence_no":self.user_query.
                value.ljust(15, ' ')}, query)
        
        # if we get an empty list as a query result notify the user
        if not results:
            npyscreen.notify_confirm("No results were found for your query.", 
                editw=1, title='Error')
            return

        # notify user of how many results they have
        npyscreen.notify_confirm("Found {} results".format(len(results)), 
            editw=1, title='Results')

        # begin the resuls with a new line
        self.results.values = ['\n']
        tickets = dict()
         
        # get column names for printing 
        column_name = self.parentApp.db.cursor.description
       
        # iterate through each record and fill in details
        for record in results:
            record_no = record[0]
            # iterate through each column in the record
            tickets[record_no] = list()
            for column_no in range(len(record)):
                if record[column_no] != None:
                    # format column name
                    c_name = column_name[column_no][0].replace("_", " ").lower().capitalize()+':'
                    tickets[record_no].append(
                        "{0: <15}{1}\n".format(c_name, str(record[column_no])))
                else:
                    c_name = column_name[column_no][0].replace("_", " ").lower().capitalize()+':'
                    tickets[record_no].append("{0: <15}{1}\n".format(c_name, "N/A"))

            tickets[record_no].append('\n')
            # append the result to the form
            self.results.values.extend(tickets[record_no])
