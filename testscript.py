import npyscreen
import cx_Oracle

class Database(object):
    def __init__(self):
        self.connnection = cx_Oracle.connect('jcairo/$Jonnyc123@gwynne.cs.ualberta.ca:1521/CRS')

# new owner form affiliated with a new vehicle registration
class NewOwnerRegForm(npyscreen.ActionPopup):
    # def afterediting(self):
    #     # prompt user, enter more owners?
    #     self.parentApp.setNextForm("MAIN")

    def create(self):
        self.owner_id = self.add(npyscreen.TitleText, name='Owner id')
        self.vehicle_id = self.add(npyscreen.TitleText,
                name='Vehicle id')
        self.is_primary_owner = self.add(npyscreen.TitleText,
                name= 'Is primary owner')
        self.is_primary_owner.value = "Y"
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    

class NewVehicleRegForm(npyscreen.ActionForm):
    def afterEditing(self):
        self.parentApp.setNextForm('OWNERFORM')

    def create(self):
        self.serial_no = self.add(npyscreen.TitleText, name='Serial no')
        self.maker = self.add(npyscreen.TitleText, name='Maker')
        self.model = self.add(npyscreen.TitleText, name='Model')
        self.year = self.add(npyscreen.TitleText, name='Year')
        self.color = self.add(npyscreen.TitleText, name='Color')
        self.type_id = self.add(npyscreen.TitleText, name='Type id')

class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        # first all caps name given is how next form
        # references other forms

        # add owner registration form
        self.addForm('OWNERFORM', NewOwnerRegForm,
                name='New Vehicle Owner Registration')

        # add vehicle reg form
        self.addForm('MAIN', NewVehicleRegForm,
                name='New Vehicle Registration')

        # register db with app
        # self.db = Database()

if __name__ == '__main__':
    TestApp = MyApplication().run()

