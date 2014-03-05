import npyscreen

class AutoTransaction(npyscreen.ActionForm):
    def create(self):
        self.seller = self.add(npyscreen.TitleText, name='Serial no:')
        self.buyer = self.add(npyscreen.TitleText, name='Maker:')
        self.date = self.add(npyscreen.TitleDateCombo, name='Date:')
        self.price = self.add(npyscreen.TitleText, name='Year:')

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
