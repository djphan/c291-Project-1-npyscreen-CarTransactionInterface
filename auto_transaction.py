import npyscreen
import datetime

class AutoTransaction(npyscreen.ActionForm):
    def create(self):
        self.t_id    = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                                name="Transaction ID:", begin_entry_at=20,
                                editable=False, color="STANDOUT")
        self.nextrely += 1
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

        # get maximum current transaction_id
        query = "SELECT MAX(transaction_id) FROM auto_sale"
        # set t_id to one greater
        self.t_id.value = str(1 + self.parentApp.db.query({}, query)[0][0])

    def validate_forms(self):
        # validate vehicle:
        query = "SELECT COUNT(serial_no) FROM vehicle WHERE serial_no = :ser"
        if self.parentApp.db.query({'ser':self.vehicle.value}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid vehicle serial number.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # validate seller:
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.seller.value}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid seller ID.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        
        # validate buyer:
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.buyer.value}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid buyer ID.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False
        
        return True
            

    def on_ok(self):
        # check for obvious illegal entries
        try:
            # are all the forms filled?
            # can price be converted to a float (with optional '$') ?
            float(self.price.value.strip('$'))

        except ValueError:
            npyscreen.notify_confirm("Price is not a valid amount of money.", title="Price Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return        

        if not self.validate_forms():
            self.editing = True
            return

        if self.date.value == '': # set date to today if unspecified
            self.date.value = datetime.date.today()

        # insert new auto transaction into table
        values = {"transaction_id" :int(self.t_id.value),
                  "seller_id"      :str(self.seller.value),
                  "buyer_id"       :str(self.buyer.value),
                  "vehicle_id"     :str(self.vehicle.value),
                  "s_date"         :self.date.value.strftime("%d-%b-%y"), # formatted for oracle
                  "price"          :float(self.price.value.strip('$'))
                  }
        prepare = "INSERT INTO auto_sale VALUES (:transaction_id, :seller_id, :buyer_id, :vehicle_id, :s_date, :price)"
        error = self.parentApp.db.insert(values, prepare)
        if error:
            # handle error
            # don't return to main menu
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        # remove old owner from table
        values = {"vehicle_id":str(self.vehicle.value)}
        prepare = "DELETE FROM owner WHERE vehicle_id = :vehicle_id"
        error = self.parentApp.db.delete(values, prepare)
        # error handling
        if error:
            # don't return to main menu
            self.editing = True
            # print error to screen
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        # insert new owner into table
        values = {"buyer_id"       :str(self.buyer.value),
                  "vehicle_id"     :str(self.vehicle.value)}
        prepare = "INSERT INTO owner VALUES (:buyer_id, :vehicle_id, 'y')"
        error = self.parentApp.db.insert(values, prepare)
        # error handling
        if error:
            # don't return to main menu
            self.editing = True
            # print error to screen
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return
        
        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
        self.parentApp.switchForm("AUTOTRANSACTION")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")
