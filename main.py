from new_vehicle_registration import NewVehicleRegistration
from auto_transaction import AutoTransaction
from driver_licence_registration import DriverLicenceRegistration
from violation_record import ViolationRecord
from search_engine import SearchEngine

main_menu = \
"""MAIN MENU: 
(1) New Vehicle Registration
(2) Auto Transaction
(3) Driver Licence Registration
(4) Violation Record
(5) Search Engine

Please enter your selection (1-5):
> """
bad_input = \
"""
Bad input.
Please enter a number from 1 to 5 to select an application.
"""
choice_set = {'1', '2', '3', '4', '5', 'q', 'Q', 'quit', 'Quit', 'QUIT'}
quit_set = {'q', 'Q', 'quit', 'Quit', 'QUIT'}

def main():
    while 1:

        choice = None
        while choice not in choice_set:
            choice = input(main_menu)
            if choice not in choice_set:
                print(bad_input)

        if choice in quit_set:
            raise SystemExit

        app = [NewVehicleRegistration(),
               AutoTransaction(),
               DriverLicenceRegistration(),
               ViolationRecord(),
               SearchEngine()
              ][int(choice)-1]

        app.run()

if __name__ == "__main__":
    main()

