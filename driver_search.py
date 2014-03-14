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
                                   begin_entry_at=21, use_two_lines=False)
        self.query_confirm = self.add(npyscreen.ButtonPress, name="Search")
        self.query_confirm.whenPressed = self.process_query

        self.backbutton = self.add(npyscreen.ButtonPress, name="Back", rely=21, relx=68)
        self.backbutton.whenPressed = lambda: self.parentApp.switchForm("SEARCHENGINE")


    def process_query(self):
        if not self.chooser.value:
            npyscreen.notify_confirm("Please select a search type.", editw=1,
                                     title='Error')
        elif self.chooser.value[0] == 0:
            pass # do name search
        elif self.chooser.value[0] == 1:
            pass # do licence number search
        


