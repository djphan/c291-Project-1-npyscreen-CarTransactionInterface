cmput-291-project-1
===================

CMPUT 291 Project 1 (Python 3)

__________________________
COMMUNICATION / NOTES     |
__________________________|
Case: Check empty database set (for the min/max queries).


Dan: The due date got pushed back to Friday 6:00 PM (in case things come up) but lets finish early.
https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=329146

!!! Test cases are up:
https://eclass.srv.ualberta.ca/mod/page/view.php?id=998610
We will have to alter some things to comply with these new requirements. Nothing too major though.

    Dan: Added some error checking to driver search, double check the work.
 	vehicle_history_search.py   <- Dan (mostly done, can you guys run tests to see if you can break this form?)
 	
If you want to work on one of them please make a note here so we don't end up doing the same thing twice.

Other TO-DO's:
  Finish error checking/validation for:
    ViolationRecord     <--} Dan: Primary key Updated. Can either of you use your database to test for additional
                             Cases. Will double check date a little later.
                           } will add people form where needed  
    AutoTransaction     <--} once it's ready - Carl
    
                        < -- Dan/Carl: Double check date time error
    NewVehicleRegistration?? (at least mostly done) <-- Jon (near completion)

  <add other TODO's here if you have any>

Jon's Notes:
The new vehicle registration form is enforcing not null constraints on
a few fields like year. Can you guys let me know if either of you have
worked on this already. If not I will fix it up.

Dan: Year may be accidently constrained. I can fix it up after I work on the other Stuff. 
Let me know what other fields should allow for NULL values. Though type ID should be a
foregin key and serial_no is a primary key.

Carl: In the "Add Owner" popup, do we need the Vehicle ID field? Shouldn't it be the same 
as the Serial No entered on the NVR form? Also we need to make sure there is exactly one 
primary owner... any ideas   on how to do that? I'm thinking either grey out the 'primary'
choice once a primary owner has been selected, or enforce that the first new owner entered 
is the primary (Enter Primary Owner: ________ ) and then have an 'Add Secondary Owner'
button?



#---------------------------------------------------------------------------------
# Manual - Auto Transaction Database Interface
#
# Table of Contents:
# i. Login
# ii. Database Entry Modules
#     ii.a. New Vehicle Registration <-- Not Done but basic part is - Dan
#     ii.b.
#     ii.c. Driver Licence Registration
#     ii.d. Violation Record
#     ii.e. People
# iii. Search
#     iii.a.
#     iii.b. Violation Search
#     iii.c. Vehicle Search History
# iv. General Information with regards to the interface
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# ii.a. New Vehicle Registration
#---------------------------------------------------------------------------------
# New Vehicle Registration will allow the user to enter data into the vehichle table.
# As well the form will prompt users to add owners to the owner table, and/or people 
# amending the people table.
#
# i. When adding to the new vehicle registration form, we will require the Serial No
# and the Type ID of the vehichle. If left blank, user will return an error indicating
# so.
# 
# ii. The Type ID of the vehicle must match information in the database.
# 
# iii. After the user inputted the vehicle information, he can add owners
# with the add owner button. The add owner button will then allow the user to
# input the new owner's SIN, vehichle serial no, and primary owner status
#
# iv. The first owner MUST be the primary owner. If the user inputs a secondary
# owner first, an error will prompt the user to enter the primary owner first.
#
# v. The user can continue to add any number of secondary owners after adding the first
# primary owner. 
#
# vi. If the owner does not exist in the database (i.e. the SIN number is not in the database)
# an error will be displayed and the user will be prompted to add the owner information
# to the people's database. A new window will popup for the people's form
#

#---------------------------------------------------------------------------------
# ii.c. Driver Licence Registration
#---------------------------------------------------------------------------------
# Driver Licence Registration allows the user to enter requisite data for entering
# a new licence into the drive_licence table. 
# 
# i. This form allows the user to register a person
# who does not currently possess a licence into the drive_licence table.
# 
# ii. If the user specifies a SIN that does not appear in the people table
# they are warned and given the option to add the person to the people table.
# They can also do this directly by hitting the add person button. After 
# the entry is complete they are forwarded back to the licence registration
# form to complete licence information and submit the form.
#
# iii. If the user chooses they may add a photo to the the entry. To do so the user 
# should navigate to the Photo field and hit enter. The user is presented with their 
# local file system and can navigate to the appropriate file. If the user wishes to
# specify a filepath directly they should hit tab once. 
# Pressing enter again submits the path to the program and brings the 
# user back to the interface to complete the licence entry.
# 
# iiii. The following fields are required: (1) Licence no (2) SIN
# 



#---------------------------------------------------------------------------------
# ii.d. Violation Record
#---------------------------------------------------------------------------------
#
# Violation Record will allow the user to enter data into the ticket table. 
# i. The basic form will allow the officer to input any driver they pull over to record
# the ticket. 
#
# ii. If the officer does not know the Violator SIN, he is able to pull up
# the primary owner of the vehicle in question using the 'Use Vehicle's Primary Owner SIN'
# button. This will query the database to obtain, and autofill the Violator SIN field with
# the primary owner's SIN. The Violator SIN field will be overrode if this option is used
# if there were any previous values entered into the field.
#
# iii. The program will auto iterate the ticket number by querying your database
# and incrementing by 1 the maximum value we can find.
#
# The following fields are required: (1) Violator SIN (2) Vehicle Serial No 
# (3) Officer SIN and (4) Violation Type due to the constraints of the database.
#
# Both SIN numbers, Vehicle Serial No, and Violation type must match pre-entered 
# data in the database. 

#---------------------------------------------------------------------------------
# iii.b. Violation Search
#---------------------------------------------------------------------------------
# Violation search allows the user to specify a SIN or licence number. Based on the
# provided value a list of all tickets from the ticket table is returned.
# Each ticket also has its fine amount which is pulled from the ticket_type table.
# The results will display:
#
# i. The number of results found
#
# ii. And an output listing: (1) The unique ticket number, 
# (2) the violator number/sin, (3) the vehicle id, (4) the officer id who issued the ticket
# (5) the violation type (6) the violation date (7) the place (8) the description
# (9) and the fine amount



#---------------------------------------------------------------------------------
# iii.c. Vehicle Search History
#---------------------------------------------------------------------------------
# Vehicle Search History will allow the user to search by Vehicle Serial No. When inputted, 
# press OK to obtain your results. The results will display:
#
# i. The number of results found
#
# ii. And an output listing: (1) The serial number of the vehicle, 
# (2) the number of sales the vehicle has been in,
# (3) the average price, and (4) the number of tickets 





