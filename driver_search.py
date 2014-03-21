import npyscreen
from npyscreen import wgwidget as widget

class DriverSearch(npyscreen.FormBaseNew):
    # to have ESC --> go back:
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
        self.chooser.values = ["Search by name", "Search by licence number"]
        self.nextrely+=1
        self.user_query = self.add(npyscreen.TitleText, name="Search Query:",
                                   begin_entry_at=15, use_two_lines=False,
                                   field_width=54)
        self.nextrely-=1
        self.query_confirm = self.add(npyscreen.ButtonPress, name="OK", relx=70)
        self.query_confirm.whenPressed = self.process_query

        self.results = self.add(npyscreen.Pager, name="Results:", height=16,
                                max_height=14, scroll_exit=True,
                                slow_scroll=True, exit_left=True,
                                exit_right=True)

    def on_ok(self):
        self.parentApp.switchForm("SEARCHENGINE")

    def process_query(self):
        if not self.chooser.value:
            npyscreen.notify_confirm("Please select a search type.", editw=1,
                                     title='Error')
            return

        if not self.user_query.value:
            npyscreen.notify_confirm("Please enter a Name or Licence Number.",
                editw=1, title='Error')
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
            results = self.parentApp.db.query({"q_name":self.user_query.value},
                                              query)

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
            results = self.parentApp.db.query(
                {"licence_no":self.user_query.value.ljust(15, ' ')}, query)

        # If we get an empty list as a query result notify the user
        if not results:
            npyscreen.notify_confirm(
                "No results were found for your query. "
                "Either Name or Licence Number does not exist in database.",
                editw=1, title='Error')
            return


        self.results.values = ['\n']
        joined = dict()
        for line in results:
            if not line[8] in joined:
                # Format output nicely:
                joined[line[8]] = list()
                joined[line[8]].append("Name:          %s\n"%line[0])
                joined[line[8]].append("Licence No:    %s\n"%(line[1], "N/A")
                                       [not line[1]])
                joined[line[8]].append("Address:       %s\n"%(line[2], "N/A")
                                       [not line[2]])
                if line[3]: joined[line[8]].append("Birthday:      %s\n"%(
                        line[3].strftime("%d-%b-%y").upper()))
                else:       joined[line[8]].append("Birthday:      N/A\n")
                joined[line[8]].append("Licence Class: %s\n"%((line[4], "N/A")
                                                              [not line[4]]))
                joined[line[8]].append("Conditions:    %s\n"%(("%s - %s"%(
                                line[5], line[6]), "N/A")[not line[5]]))
                if line[7]: joined[line[8]].append("Expiring Date: %s\n"%(
                        line[7].strftime("%d-%b-%y").upper()))
                else:       joined[line[8]].append("Expiring Date: N/A\n")
                joined[line[8]].append('\n')
            else:
                joined[line[8]].insert(-2, ' '*15+'%s\n'%('%s - %s'%(
                            line[5], line[6]), "N/A")[not line[5]])

        for person in joined:
            self.results.values.extend(joined[person])
        npyscreen.notify_confirm(str(len(joined))+" result"+('s','')
                                 [len(joined)==1]+" found.", editw=1, title='')
