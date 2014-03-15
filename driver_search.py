import npyscreen

class DriverSearch(npyscreen.ActionFormCarl):
    def create(self):

        # self.backbutton.whenPressed = lambda: self.parentApp.switchForm("SEARCHENGINE")
        # self.tmp = self.add(npyscreen.TitleText)
        
        self.chooser = self.add(npyscreen.SelectOne, max_height=2,
                                scroll_exit=True)
        self.chooser.values = ["Search by name", "Search by licence number"]
        self.nextrely+=1
        # NOTE: When an entry is selected, the value of self.chooser.value will
        # be a list containing the index of the entry in the above list - in
        # this example, [0] or [1]. If nothing is selected, self.chooser.value
        # will be [].

        self.user_query = self.add(npyscreen.TitleText, name="Search Query:",
                                   begin_entry_at=15, use_two_lines=False, field_width=54)
        self.nextrely-=1
        self.query_confirm = self.add(npyscreen.ButtonPress, name="OK", relx=70)
        self.query_confirm.whenPressed = self.process_query

        self.results = self.add(npyscreen.Pager, name="Results:", height=18,
                                max_height=18, scroll_exit=True,
                                slow_scroll=True, exit_left=True, exit_right=True)
        
    def on_ok(self):
        self.parentApp.switchForm("SEARCHENGINE")        

    def process_query(self):
        if not self.chooser.value:
            npyscreen.notify_confirm("Please select a search type.", editw=1,
                                     title='Error')
            return

        if self.chooser.value[0] == 0:
            query = """
SELECT p.name, l.licence_no, p.addr, p.birthday, l.class, c.c_id, 
        c.description, l.expiring_date, p.sin
FROM people p, drive_licence l, driving_condition c, restriction r
WHERE p.sin = l.sin(+) AND
      l.licence_no = r.licence_no(+) AND
      r.r_id = c.c_id(+) AND
      UPPER(p.name) = UPPER(:q_name)
            """
            results = self.parentApp.db.query({"q_name":self.user_query.value}, query)

        elif self.chooser.value[0] == 1:
            query = """
SELECT p.name, l.licence_no, p.addr, p.birthday, l.class, c.c_id, 
        c.description, l.expiring_date, p.sin
FROM people p, drive_licence l, driving_condition c, restriction r
WHERE p.sin = l.sin(+) AND
      l.licence_no = r.licence_no(+) AND
      r.r_id = c.c_id(+) AND
      UPPER(l.licence_no) = UPPER(:licence_no)
            """
            results = self.parentApp.db.query({"licence_no":self.user_query.value.ljust(15, ' ')}, query)

        self.results.values = ['\n']
        joined = dict()
        for line in results:
            if not line[8] in joined:
                joined[line[8]] = list()
                joined[line[8]].append("Name:          %s\n"%line[0])                              
                joined[line[8]].append("Licence No:    %s\n"%(line[1], "N/A")[not line[1]])
                joined[line[8]].append("Address:       %s\n"%(line[2], "N/A")[not line[2]])
                if line[3]: joined[line[8]].append("Birthday:      %s\n"%line[3].strftime("%d-%b-%y").upper())
                else:       joined[line[8]].append("Birthday:      N/A\n")
                joined[line[8]].append("Licence Class: %s\n"%((line[4], "N/A")[not line[4]]))
                joined[line[8]].append("Conditions:    %s\n"%(("%s - %s"%(line[5], line[6]), "N/A")[not line[5]]))
                if line[7]: joined[line[8]].append("Expiring Date: %s\n"%line[7].strftime("%d-%b-%y").upper())
                else:       joined[line[8]].append("Expiring Date: N/A\n")
                joined[line[8]].append('\n')                                                       
            else:
                joined[line[8]].insert(-2, '               %s\n'%('%s - %s'%(line[5], line[6]), "N/A")[not line[5]])

        for person in joined:
            self.results.values.extend(joined[person])
        npyscreen.notify_confirm(str(len(results))+(" results found."," result found.")[len(results)==1],
                                 editw=1, title='')

        


