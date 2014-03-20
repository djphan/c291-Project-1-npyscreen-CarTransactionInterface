import npyscreen
import datetime

class AddBuyer(npyscreen.ActionPopup):
    def create(self):
        self.buyer_id = self.add(npyscreen.TitleText, name="Buyer ID:")

    def on_ok(self):
        
        # is this buyer in the database?
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        
        if self.parentApp.db.query({'sin':self.buyer_id.value.strip('\n').ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Buyer %s not in database.\nPlease enter buyer information."%self.buyer_id.value, title="Alert", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                # if not, prompt to enter buyer information, then add buyer to database and continue
            self.parentApp.AP_default = self.buyer_id.value
            if not self.buyer_id.value in self.parentApp.AT_buyers:
                self.parentApp.AT_buyers.append(self.buyer_id.value)
            self.parentApp.switchForm("ADDPERSON")

        else:
            if not self.buyer_id.value in self.parentApp.AT_buyers:
                self.parentApp.AT_buyers.append(self.buyer_id.value)
            self.buyer_id.value = ''
            self.parentApp.switchForm("AUTOTRANSACTION")

    def on_cancel(self):
        # if we didn't end up putting the buyer in the database, then take him
        # back out of the buyer list.
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.buyer_id.value.ljust(15, ' ')}, query)[0][0] == 0 and self.buyer_id.value in self.parentApp.AT_buyers:
            self.parentApp.AT_buyers.remove(self.buyer_id.value)
        self.buyer_id.value = '' # clear the form
        self.parentApp.switchForm("AUTOTRANSACTION")
        
class AutoTransaction(npyscreen.FormBaseNew):
    def create(self):
        self.nextrelx+=1
        self.t_id    = self.add(npyscreen.TitleFixedText, use_two_lines=False,
                                name="Transaction ID:", begin_entry_at=20,
                                editable=False, color="STANDOUT")
        self.nextrely+=1;
        self.vehicle = self.add(npyscreen.TitleText, use_two_lines=False,
                                name='Vehicle Serial no:', begin_entry_at=20)
        self.date    = self.add(npyscreen.TitleDateCombo,
                                name='Date:', begin_entry_at=20)
        self.price   = self.add(npyscreen.TitleText,
                                name='Price:', begin_entry_at=20)
        self.seller  = self.add(npyscreen.TitleText,
                                name='Seller:', begin_entry_at=20)

        self.primary_buyer  = self.add(npyscreen.TitleText,
                                name='Primary Buyer:', begin_entry_at=20)
        # self.primary_buyer.when_cursor_moved = self.check_primary


############
        self.nextrely+=1
        self.buyersTitle2 = self.add(npyscreen.TitleFixedText, name="Other Buyer(s):", editable=False, max_width=16)
        self.nextrelx-=2
        self.nextrely-=1
        # self.add_seller = self.add(npyscreen.ButtonPress, name="Add Seller", width=10)
        # self.add_seller.whenPressed = lambda: self.parentApp.switchForm("ADDSELLER")
        self.add_buyer = self.add(npyscreen.ButtonPress, name="Add Buyer", width=10)
        self.add_buyer.whenPressed = lambda: self.parentApp.switchForm("ADDBUYER")
        self.nextrelx+=2

        self.nextrely-=2; self.nextrelx+=20
        self.other_buyers = self.add(npyscreen.Pager, name="buyers", height=10, editable=False,
                                max_height=10, width=16, max_width=16, scroll_exit=True, slow_scroll=True)
        self.parentApp.AT_buyers = list()
        self.other_buyers.values = self.parentApp.AT_buyers


        self.nextrelx+=32; self.nextrely+=1
        self.submit_button = self.add(npyscreen.ButtonPress, name="Submit", width=8)
        self.submit_button.whenPressed = self.on_ok
        self.nextrely-=1; self.nextrelx+=10
        self.cancel_button = self.add(npyscreen.ButtonPress, name="Cancel", width=8)
        self.cancel_button.whenPressed = self.on_cancel
        self.nextrelx-=8

        # get maximum current transaction_id
        query = "SELECT MAX(transaction_id) FROM auto_sale"
        # set t_id to one greater
        # if max returns none due to an unpopulated database
        # catch the exception that occurs on the addition
        # and explicitly set the first t_id to a 1.
        try:
            self.t_id.value = str(1 + self.parentApp.db.query({}, query)[0][0])
        except TypeError:
            self.t_id.value = 1

    def validate_forms(self):
        # is there a vehicle entered?
        if not self.vehicle.value:
            npyscreen.notify_confirm("Enter a vehicle serial number.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # validate vehicle:
        query = "SELECT COUNT(serial_no) FROM vehicle WHERE serial_no = :ser"
        if self.parentApp.db.query({'ser':self.vehicle.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Invalid vehicle serial number.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # set date to today if unspecified            
        if self.date.value == '':
            self.date.value = datetime.date.today()

        # can price be converted to a float (with optional '$') ?
        try:
            float(self.price.value.strip('$'))
        except ValueError:
            npyscreen.notify_confirm("Price is not a valid amount of money.", title="Price Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # is there a seller entered?
        if not self.seller.value:
            npyscreen.notify_confirm("Enter a seller ID.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # validate seller:
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.seller.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Seller %s is not in database."%self.seller.value, title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # does seller own vehicle?
        query = "SELECT COUNT(*) FROM owner WHERE owner_id = :o_id AND vehicle_id = :v_id"
        if self.parentApp.db.query({'o_id':self.seller.value.ljust(15, ' '),
                                    'v_id':self.vehicle.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Seller %s cannot sell vehicle %s because he/she is not a registered owner."%(self.seller.value,self.vehicle.value), title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # is there a primary buyer entered?
        if not self.primary_buyer.value:
            npyscreen.notify_confirm("Enter a primary buyer ID.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return False

        # is the primary buyer in the database? if not, prompt to add buyer.
        query = "SELECT COUNT(sin) FROM people WHERE sin = :sin"
        if self.parentApp.db.query({'sin':self.primary_buyer.value.ljust(15, ' ')}, query)[0][0] == 0:
            npyscreen.notify_confirm("Primary buyer %s not found in database.\nPlease enter buyer information."%self.primary_buyer.value, title="Alert", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.parentApp.AP_default = self.primary_buyer.value
            self.parentApp.switchForm("ADDPERSON")
            return False
        return True

        # no need to check secondary buyers, this was done by add buyer

        return True
            
    def on_ok(self):
            
        if not self.validate_forms():
            # self.editing = True
            return


        # insert new auto transaction into table
        

        values = {"transaction_id" :int(self.t_id.value),
                  "seller_id"      :self.seller.value,
                  "buyer_id"       :self.primary_buyer.value,
                  "vehicle_id"     :self.vehicle.value,
                  "s_date"         :self.date.value.strftime("%d-%b-%y"), # formatted for oracle
                  "price"          :float(self.price.value.strip('$'))
                  }
        prepare = "INSERT INTO auto_sale VALUES (:transaction_id, :seller_id, :buyer_id, :vehicle_id, :s_date, :price)"
        error = self.parentApp.db.insert(values, prepare)
        if error:
            self.editing = True # display error, and don't return to main menu
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        # remove old owner(s) from table
        values = {"vehicle_id":self.vehicle.value}
        prepare = "DELETE FROM owner WHERE vehicle_id = :vehicle_id"
        error = self.parentApp.db.delete(values, prepare)
        if error:
            self.editing = True
            npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            return

        # insert new owners into table
        for buyer in [self.primary_buyer.value] + self.other_buyers.values:
            values = {"buyer_id"       :buyer,
                      "vehicle_id"     :self.vehicle.value,
                      "y_or_n"         :'y' if buyer == self.primary_buyer.value else 'n'
                     } 
            prepare = "INSERT INTO owner VALUES (:buyer_id, :vehicle_id, :y_or_n)"
            error = self.parentApp.db.insert(values, prepare)
            # error handling
            if error:
                self.editing = True
                npyscreen.notify_confirm(str(error), title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                return
        
        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)

        # get maximum current transaction_id
        query = "SELECT MAX(transaction_id) FROM auto_sale"
        # increment t_id based on largest t_id in db
        # if there are no t_id's in the db catch the conversion
        # error that occurs when trying to increment a none
        # type and set the first t_id to 1
        try:
            self.t_id.value = str(1 + self.parentApp.db.query({}, query)[0][0])
        except TypeError:
            self.t_id.value = 1
        self.parentApp.AT_buyers = list()
        self.other_buyers.values = self.parentApp.AT_buyers
        self.vehicle.value = ''
        self.date.value = ''
        self.price.value = ''
        self.seller.value = ''
        self.primary_buyer.value = ''

    def on_cancel(self):
        self.parentApp.AT_buyers = list()
        self.other_buyers.values = self.parentApp.AT_buyers
        self.vehicle.value = ''
        self.date.value = ''
        self.price.value = ''

        self.parentApp.setNextForm("MAIN")
        self.editing=False
        # self.parentApp.removeForm("AUTOTRANSACTION")
        self.parentApp.addForm('AUTOTRANSACTION',
                     AutoTransaction, name='Auto Transaction')
