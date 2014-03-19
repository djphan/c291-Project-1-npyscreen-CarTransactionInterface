#!/usr/bin/python3

import npyscreen
import cx_Oracle
import pdb
from new_vehicle_registration import NewVehicleRegistration
from auto_transaction import AutoTransaction, AddBuyer
from driver_licence_registration import DriverLicenceRegistration
from violation_record import ViolationRecord
from search_engine import SearchEngine
from add_owner_on_vehicle import AddOwnerOnVehicle
from database import Database
from driver_search import DriverSearch
from violation_search import ViolationSearch
from vehicle_history_search import VehicleHistorySearch    
from add_people import AddPerson        

class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):

        self.db = Database()   # empty Database object with db.logged_in = False
        self.addFormClass('MAIN', MainMenu, name="MAIN MENU")
        self.addFormClass('MAIN_POPUP',
                     MainMenuPopup, name="Connect to Oracle")
        self.addFormClass('NEWVEHICLEREGISTRATION',
                     NewVehicleRegistration, name='New Vehicle Registration')

        self.auto_transaction_initialized = False
        self.addForm('ADDBUYER', AddBuyer, name='Add Buyer')
        # self.addFormClass('ADDSELLER', AddSeller, name='Add Seller') # not need anymore?



        self.addFormClass('DRIVERLICENCEREGISTRATION',
                     DriverLicenceRegistration, name='Driver Licence Registration')
        self.addFormClass('VIOLATIONRECORD',
                     ViolationRecord, name='Violation Record')
        self.addFormClass('SEARCHENGINE',
                     SearchEngine, name='Search Engine')
        self.addFormClass('DRIVER_SEARCH',
                     DriverSearch, name='Driver Search')
        self.addForm('ADDOWNERONVEHICLE',
                     AddOwnerOnVehicle, name='Add owner')
        self.addFormClass('VIOLATION_SEARCH',
                     ViolationSearch, name='Violation Search')
        self.addFormClass('VEHICLE_HISTORY_SEARCH',
                     VehicleHistorySearch, name='Vehicle History Search')

        # new additions for add people popup form
        self.addFormClass('ADDPERSON', AddPerson, name='Add Person', minimum_lines=24, minimum_columns=80, lines=16, columns=60)
        self.AP_default = None

class MainMenuPopup(npyscreen.ActionPopup):
    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Oracle user:")
        self.username.value = 'sobolews'
        self.password = self.add(npyscreen.TitlePassword, name="Password:")
        self.password.value = '2Ajtja.a'
        self.host = self.add(npyscreen.TitleText, name="Host:")
        self.host.value = "@gwynne.cs.ualberta.ca:1521/CRS"

    def on_ok(self):
        try:
            self.parentApp.db = Database("%s/%s%s" % (self.username.value,
                                                      self.password.value,
                                                      self.host.value))
        except cx_Oracle.DatabaseError:
            self.parentApp.db = Database()
            self.parentApp.switchForm("MAIN_POPUP")
        else:
            self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class MainMenu(npyscreen.FormBaseNew):
    def notify_not_logged_in(self):
        npyscreen.notify_confirm("Please log in to Oracle Database first!", title="No Database Connection", form_color='STANDOUT', wrap=True, wide=False, editw=1)
        self.parentApp.switchForm("MAIN")

    def create(self):
        def buttonpress0(*args):
            self.parentApp.switchForm("MAIN_POPUP")
        def buttonpress1(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("NEWVEHICLEREGISTRATION")
            else: self.notify_not_logged_in()
        def buttonpress2(*args):
            if self.parentApp.db.logged_in:
                if not self.parentApp.auto_transaction_initialized:
                    self.parentApp.addForm('AUTOTRANSACTION', AutoTransaction, name='Auto Transaction')
                    self.parentApp.auto_transaction_initialized = True
                self.parentApp.switchForm("AUTOTRANSACTION")
            else: self.notify_not_logged_in()
        def buttonpress3(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("DRIVERLICENCEREGISTRATION")
            else: self.notify_not_logged_in()
        def buttonpress4(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("VIOLATIONRECORD")
            else: self.notify_not_logged_in()
        def buttonpress5(*args):
            if self.parentApp.db.logged_in: self.parentApp.switchForm("SEARCHENGINE")
            else: self.notify_not_logged_in()
        def buttonpress6(*args):
            self.parentApp.setNextForm(None)
            self.editing = False

        self.button0 = self.add(npyscreen.ButtonPress, name="Oracle Login")
        self.button0.whenPressed = buttonpress0
        self.nextrely += 1 
        self.button1 = self.add(npyscreen.ButtonPress, name="New Vehicle Registration")
        self.button1.whenPressed = buttonpress1
        self.button2 = self.add(npyscreen.ButtonPress, name="Auto Transaction")
        self.button2.whenPressed = buttonpress2
        self.button3 = self.add(npyscreen.ButtonPress, name="Driver Licence Registration")
        self.button3.whenPressed = buttonpress3
        self.button4 = self.add(npyscreen.ButtonPress, name="Violation Record")
        self.button4.whenPressed = buttonpress4
        self.button5 = self.add(npyscreen.ButtonPress, name="Search Engine")
        self.button5.whenPressed = buttonpress5
        self.nextrely += 1
        self.button6 = self.add(npyscreen.ButtonPress, name="Quit",)
        self.button6.whenPressed = buttonpress6

if __name__ == "__main__":
    app = MyApplication()
    app.run()
    print('done')
