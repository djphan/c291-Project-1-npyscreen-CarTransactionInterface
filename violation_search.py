import npyscreen
from npyscreen import wgwidget as widget

class ViolationSearch(npyscreen.FormBaseNew):
    """
    Form to search the database for ticket information.

    Required input:
      Search type selection
      Search query

    Returns:
      Ticket no
      Violator no
      Vehicle ID
      Officer No
      Vtype
      Vdate
      Place
      Descriptions
      Fine
    """
    # ESC --> go back:
    def set_up_exit_condition_handlers(self):
        super().set_up_exit_condition_handlers()
        self.how_exited_handers.update({
            widget.EXITED_ESCAPE:   self.on_ok
        })

    def create(self):
        self.backbutton = self.add(npyscreen.ButtonPress, name="Back")
        self.backbutton.whenPressed = self.on_ok
        self.nextrely+=1
        self.chooser = self.add(npyscreen.SelectOne, max_height=2,
                                scroll_exit=True)
        self.chooser.values = ["Search by SIN", "Search by licence number"]
        self.nextrely+=1
        self.user_query = self.add(npyscreen.TitleText, name="Search Query:",
                                   begin_entry_at=15, use_two_lines=False, 
                                   field_width=54)
        self.nextrely-=1   
        self.query_confirm = self.add(npyscreen.ButtonPress, name="OK", relx=70,
                                      scroll_exit = True)
        self.query_confirm.whenPressed = self.process_query

        self.results = self.add(npyscreen.Pager, name="Results:", height=14,
                                max_height=14, scroll_exit=True,
                                slow_scroll=True, exit_left=True,
                                exit_right=True)
        
    def on_ok(self):
        self.parentApp.switchForm("SEARCHENGINE")        

    def process_query(self):
        # ensure user has selected search type
        if not self.chooser.value:
            npyscreen.notify_confirm("Please select a search type.", editw=1,
                                     title='Error')
            return
        
        if not self.user_query.value:
            npyscreen.notify_confirm("Please enter a SIN or licence number.", 
                                     editw=1, title='Error')
            return
    
        # Build query for when user picks "Search by sin"
        if self.chooser.value[0] == 0:
            query = """
                SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no,
                       t.vtype, t.vdate, t.place, t.descriptions, tt.fine
                FROM ticket t, ticket_type tt
                WHERE tt.vtype (+)= t.vtype
                      AND UPPER(t.violator_no) = UPPER(:violator_no)
            """
            results = self.parentApp.db.query({"violator_no":self.user_query.
                value.ljust(15, ' ')}, query)
        
        # build query for when user selects "Search by licence number"
        elif self.chooser.value[0] == 1:
            query = """
                SELECT t.ticket_no, t.violator_no, t.vehicle_id, t.office_no,
                       t.vtype, t.vdate, t.place, t.descriptions, tt.fine
                FROM ticket t, ticket_type tt, drive_licence d
                WHERE tt.vtype (+)= t.vtype
                      AND UPPER(d.licence_no) = UPPER(:licence_no)
                      AND d.sin (+)= t.violator_no
            """
            results = self.parentApp.db.query({"licence_no":self.user_query.
                value.ljust(15, ' ')}, query)
        
        # If we get an empty list as a query result notify the user
        if not results:
            npyscreen.notify_confirm("No results were found for your query.", 
                editw=1, title='Error')
            return

        # Notify user of how many results they have
        npyscreen.notify_confirm("Found {} results".format(len(results)), 
            editw=1, title='Results')

        # Begin the resuls with a new line
        self.results.values = ['\n']
        tickets = dict()
         
        # Get column names for printing 
        column_name = self.parentApp.db.cursor.description
       
        # Iterate through each record and fill in details
        for record in results:
            record_no = record[0]
            # Iterate through each column in the record
            tickets[record_no] = list()
            for column_no in range(len(record)):
                if record[column_no] != None:
                    # Format column name
                    c_name = \
            column_name[column_no][0].replace("_", " ").lower().capitalize()+':'
                    tickets[record_no].append(
                        "{0: <15}{1}\n".format(c_name, str(record[column_no])))
                else:
                    c_name = \
            column_name[column_no][0].replace("_", " ").lower().capitalize()+':'
                    tickets[record_no].append(
                        "{0: <15}{1}\n".format(c_name, "N/A"))
                    

            tickets[record_no].append('\n')
            # Append the result to the form
            self.results.values.extend(tickets[record_no])
