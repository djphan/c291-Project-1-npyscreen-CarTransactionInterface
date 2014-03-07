import npyscreen

class AutoTransaction(npyscreen.ActionForm):
    def create(self):
        self.vehicle = self.add(npyscreen.TitleText, use_two_lines=False,
                                name='Vehicle Serial no:', begin_entry_at=20)
        self.seller  = self.add(npyscreen.TitleText,
                                name='Seller:', begin_entry_at=20)
        self.buyer   = self.add(npyscreen.TitleText,
                                name='Buyer:', begin_entry_at=20)
        self.date    = self.add(npyscreen.TitleDateCombo,
                                name='Date:', begin_entry_at=20)
        self.price   = self.add(npyscreen.TitleText,
                                name='Price:', begin_entry_at=20)

    def on_ok(self):
        self.parentApp.switchFormPrevious()
        with open('output.txt', 'w') as fout:
            print(self.vehicle.value, file=fout)
            print(self.seller.value, file=fout)
            print(self.buyer.value, file=fout)
            print(self.date.value, file=fout)
            print(self.price.value, file=fout)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
