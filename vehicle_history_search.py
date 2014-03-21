import npyscreen
from npyscreen import wgwidget as widget

class VehicleHistorySearch(npyscreen.FormBaseNew):
    """
    Form to search the database for a vehicle's history statistics.

    Required input:
      Serial No

    Returns:
      Serial No
      Number of Sales
      Average price
      Number of tickets
    """
    def set_up_exit_condition_handlers(self):
        super().set_up_exit_condition_handlers()
        self.how_exited_handers.update({
            widget.EXITED_ESCAPE:   self.on_ok
        })

    def create(self):
        self.backbutton = self.add(npyscreen.ButtonPress, name="Back")
        self.backbutton.whenPressed = self.on_ok
        self.nextrely+=1
        self.serial_no = self.add(npyscreen.TitleText,
                                  name='Search by Vehicle Serial No',
                                  editable=False, begin_entry_at=20)
        self.user_query = self.add(npyscreen.TitleText, name="Search Query:",
                                   begin_entry_at=15, use_two_lines=False, 
                                   field_width=54)
        self.nextrely-=1
        self.query_confirm = self.add(npyscreen.ButtonPress, name="OK", relx=70)
        self.query_confirm.whenPressed = self.process_query

        self.results = self.add(npyscreen.Pager, name="Results:", height=10,
                                max_height=10, scroll_exit=True,
                                slow_scroll=True, exit_left=True,
                                exit_right=True)

    def on_ok(self):
        self.parentApp.switchForm("SEARCHENGINE")  

    def process_query(self):
        if not self.user_query.value:
            npyscreen.notify_confirm("Please enter a vehicle serial no.", 
                editw=1, title='Error')
            return
    
        # Build query for when user picks "Search by vehicle serial no"
        query = """ 
            SELECT  h.serial_no AS Serial_No,
                    COUNT(DISTINCT transaction_id) AS Number_of_Sales,
                    AVG(price) AS Average_Price,
                    COUNT(DISTINCT t.ticket_no) AS Number_of_Tickets 
            FROM    vehicle h, auto_sale a, ticket t
            WHERE   t.vehicle_id (+)= h.serial_no AND
                    a.vehicle_id (+)= h.serial_no AND
                    UPPER(:serial_no) = UPPER(h.serial_no)
            GROUP BY h.serial_no
          """
        results = self.parentApp.db.query(
            {"serial_no":self.user_query.value.ljust(15, ' ')}, query)

        # If we get an empty list as a query result notify the user
        if not results:
            npyscreen.notify_confirm(
                "No results were found for your query. "
                "Vehicle Serial No does not exist in database", 
                editw=1, title='Error')
            return

        # begin the resuls with a new line
        self.results.values = ['\n']
        joined = dict()
         
        # get column names for printing 
        column_name = self.parentApp.db.cursor.description
       
        # iterate through each record and fill in details
        for record in results:
            record_no = record[0]
            # iterate through each column in the record
            joined[record_no] = list()
            for column_no in range(len(record)):
                if record[column_no] != None:
                    # format column name
                    c_name = \
            column_name[column_no][0].replace("_", " ").lower().capitalize()+':'
                    if column_no == 2:
                        joined[record_no].append("{0: <20} ${1}\n".format(
                                c_name, str(round(record[column_no], 2))))
                    else:
                        joined[record_no].append(
                        "{0: <20} {1}\n".format(c_name, str(record[column_no])))
                else:
                    c_name = \
            column_name[column_no][0].replace("_", " ").lower().capitalize()+':'
                    joined[record_no].append("{0: <20} {1}\n".format(c_name,
                                                                     "N/A"))
            joined[record_no].append('\n')
            # Append the result to the form
            self.results.values.extend(joined[record_no])
