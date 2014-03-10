#!/usr/bin/python3

import npyscreen
import cx_Oracle
import pdb
from new_vehicle_registration import NewVehicleRegistration
from auto_transaction import AutoTransaction
from driver_licence_registration import DriverLicenceRegistration
from violation_record import ViolationRecord
from search_engine import SearchEngine
from database import Database
    
        
class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):

        self.addFormClass('MAIN', MainMenu, name="MAIN MENU")
        self.addForm('MAIN_POPUP', MainMenuPopup,
                     name="Connect to Oracle")

        self.addFormClass('NEWVEHICLEREGISTRATION',
                     NewVehicleRegistration, name='New Vehicle Registration')
        self.addFormClass('AUTOTRANSACTION',
                     AutoTransaction, name='Auto Transaction')
        self.addFormClass('DRIVERLICENCEREGISTRATION',
                     DriverLicenceRegistration, name='Driver Licence Registration')
        self.addFormClass('VIOLATIONRECORD',
                     ViolationRecord, name='Violation Record')
        self.addFormClass('SEARCHENGINE',
                     SearchEngine, name='Search Engine')
        self.db = None

class MainMenuPopup(npyscreen.ActionPopup):
    def create(self):
        self.username = self.add(npyscreen.TitleText, name="Oracle user:")
        self.username.value = ''
        self.password = self.add(npyscreen.TitlePassword, name="Password:")
        self.password.value = ''
        self.host = self.add(npyscreen.TitleText, name="Host:")
        self.host.value = "@gwynne.cs.ualberta.ca:1521/CRS"

    def on_ok(self):
        try:
            self.parentApp.db = Database("%s/%s%s" % (self.username.value,
                                                      self.password.value,
                                                      self.host.value))
        except cx_Oracle.DatabaseError:
            npyscreen.notify_confirm("Invalid login, please try again.", title="Error", form_color='STANDOUT', wrap=True, wide=False, editw=1)
            self.editing = True
            return
        
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class MainMenu(npyscreen.FormBaseNew):
    def create(self):
        def buttonpress0(*args):
            self.parentApp.switchForm("MAIN_POPUP")
        def buttonpress1(*args):
            if self.parentApp.db:
                self.parentApp.switchForm("NEWVEHICLEREGISTRATION")
            else:
                npyscreen.notify_confirm("Please log in to Oracle Database first!", title="No Database Connection", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                self.parentApp.switchForm("MAIN")
        def buttonpress2(*args):
            if self.parentApp.db:
                self.parentApp.switchForm("AUTOTRANSACTION")
            else:
                npyscreen.notify_confirm("Please log in to Oracle Database first!", title="No Database Connection", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                self.parentApp.switchForm("MAIN")
        def buttonpress3(*args):
            if self.parentApp.db:
                self.parentApp.switchForm("DRIVERLICENCEREGISTRATION")
            else:
                npyscreen.notify_confirm("Please log in to Oracle Database first!", title="No Database Connection", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                self.parentApp.switchForm("MAIN")
        def buttonpress4(*args):
            if self.parentApp.db:
                self.parentApp.switchForm("VIOLATIONRECORD")
            else:
                npyscreen.notify_confirm("Please log in to Oracle Database first!", title="No Database Connection", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                self.parentApp.switchForm("MAIN")
        def buttonpress5(*args):
            if self.parentApp.db:
                self.parentApp.switchForm("SEARCHENGINE")
            else:
                npyscreen.notify_confirm("Please log in to Oracle Database first!", title="No Database Connection", form_color='STANDOUT', wrap=True, wide=False, editw=1)
                self.parentApp.switchForm("MAIN")
        def buttonpress6(*args):
            self.parentApp.setNextForm(None)
            self.editing = False

        self.button0 = self.add(npyscreen.ButtonPress, name="Oracle Login", rely=2)
        self.button0.whenPressed = buttonpress0
        self.button1 = self.add(npyscreen.ButtonPress, name="New Vehicle Registration", rely=4)
        self.button1.whenPressed = buttonpress1
        self.button2 = self.add(npyscreen.ButtonPress, name="Auto Transaction", rely=5)
        self.button2.whenPressed = buttonpress2
        self.button3 = self.add(npyscreen.ButtonPress, name="Driver Licence Registration", rely=6)
        self.button3.whenPressed = buttonpress3
        self.button4 = self.add(npyscreen.ButtonPress, name="Violation Record", rely=7)
        self.button4.whenPressed = buttonpress4
        self.button5 = self.add(npyscreen.ButtonPress, name="Search Engine", rely=8)
        self.button5.whenPressed = buttonpress5
        self.button6 = self.add(npyscreen.ButtonPress, name="Quit", rely=10)
        self.button6.whenPressed = buttonpress6

if __name__ == "__main__":
    app = MyApplication()
    app.run()
    print('done')
