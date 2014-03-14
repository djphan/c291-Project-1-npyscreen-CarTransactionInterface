import curses
import npyscreen

class DriverSearch(npyscreen.FormBaseNew):
    def create(self):

        self.chooser = self.add(npyscreen.SelectOne, max_height=3,
                                scroll_exit=True)
        self.chooser.values = ["Search by name", "Search by licence number"]
        # NOTE: When an entry is selected, the value of self.chooser.value will
        # be a list containing the index of the entry in the above list - in
        # this example, [0] or [1]. If nothing is selected, self.chooser.value
        # will be [].

        self.user_query = self.add(npyscreen.TitleText, name="Enter Search Query:",
                                   begin_entry_at=21, use_two_lines=False, field_width=35)

        self.query_confirm = self.add(npyscreen.ButtonPress, name="Search", rely=5, relx=60)
        self.query_confirm.whenPressed = self.process_query

        self.results = self.add(npyscreen.Pager, name="Results:", height=2,
                                max_height=10, scroll_exit=True,
                                slow_scroll=True, exit_left=True, exit_right=True)

        self.backbutton = self.add(npyscreen.ButtonPress, name="Back", rely=21, relx=68)
        self.backbutton.whenPressed = lambda: self.parentApp.switchForm("SEARCHENGINE")
        

        



    def process_query(self):
        if not self.chooser.value:
            npyscreen.notify_confirm("Please select a search type.", editw=1,
                                     title='Error')
        elif self.chooser.value[0] == 0:
            query = """SELECT * FROM people WHERE name = :q_name"""
            self.results.values = self.parentApp.db.query({"q_name":self.user_query.value}, query)
            npyscreen.notify_confirm(str(self.results.values), editw=1,
                                     title='Results')
            

            pass # do name search
        elif self.chooser.value[0] == 1:
            pass # do licence number search
        


