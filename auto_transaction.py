import npyscreen

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

    def on_ok(self):
        # check for obvious illegal entries
        try:
            # are all the forms filled?
            assert all([self.vehicle.value, self.seller.value, 
                        self.buyer.value, self.date.value, self.price.value])
            # can price be converted to a float (with optional '$') ?
            float(self.price.value.strip('$'))

        except AssertionError:
            npyscreen.notify_confirm("Please fill in all info before submitting.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return        

        except ValueError:
            npyscreen.notify_confirm("Price is not a valid amount of money.", title="Price Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return        

        # DEBUG: 
        # fout = open("output.txt", 'w')
        # print(self.vehicle.value, file=fout)
        # print(self.seller.value, file=fout)
        # print(self.buyer.value, file=fout)
        # print(self.date.value, file=fout)
        # print(type(self.date.value), self.date.value.strftime("%d-%b-%y"), file=fout)
        # print(self.price.value, self.price.value.strip('$'), file=fout)
        # print("T_ID:", self.t_id.value, file=fout)

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
            print(error, file=fout)
            print(error.code, file=fout)
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
        
        # if all of the above succeeded:
        # increment next t_id
        # self.t_id.value = str(int(self.t_id.value) + 1)

        # Add option to do another transaction in this form???
        npyscreen.notify_confirm("Success!", title="Status", form_color='STANDOUT', wrap=True, wide=False, editw=1)
        self.parentApp.switchFormPrevious()



    def on_cancel(self):
        self.parentApp.switchFormPrevious()
