cmput-291-project-1
===================

CMPUT 291 Project 1 (Python 3)

#---------------------------------------------------------------------------------
# Manual - Auto Transaction Database Interface
#
# Table of Contents:
# i. Login
# ii. Database Entry Modules
#     ii.a. New Vehicle Registration 
#     ii.b. Auto Transaction
#     ii.c. Driver Licence Registration
#     ii.d. Violation Record
#     ii.e. People <- Not Done
# iii. Search
#     iii.a. Driver Search
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
# input the new owner's SIN, vehichle serial no, and primary owner status.
#
# iv. The user can input the owners in any order, however a primary owner must 
# be specified before the information is entered into the database. An error prompt
# will be raised if the user does not complete this action.
#
# The owner form will auto fill the vehicle serial no for each entry.
#
# v. If the owner does not exist in the database (i.e. the SIN number is not in the database)
# an error will be displayed and the user will be prompted to add the owner information
# to the people's database. A new window will popup for the people's form. The user can fill
# in the form and return to the add owner form to complete it.
#

#---------------------------------------------------------------------------------
# ii.b. Auto Transaction
#---------------------------------------------------------------------------------
# Auto transaction allows the user to enter the requisite data for auto sale
# transactions.
# 
# i. The Vehicle serial number field must match a vehicle in the vehicle table
# 
# ii. The user must enter Seller and Buyer sins that match those in the people table.
# The sins specified must be associated with the vehicle in the owner table.
# 
# iii. If the user wishes to add additional buyers they can be added via
# the "Add buyer button" 
# 
# iv. The Transaction Id field is populated by incrementing the max transacion
# id in the db.
# 
# v. Upon creating successfull transaction the seller is removed as an owner
# of the vehicle in the owner table, the new owner is added and the transaction
# details are entered into the auto sales table.
# 
# vi. All fields other than the date field must be populated b the user
# to create a succesfull transaction.


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
# iv. The following fields are required: (1) Licence no (2) SIN

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
# and incrementing by the max value by 1..
#
# The following fields are required: (1) Violator SIN (2) Vehicle Serial No 
# (3) Officer SIN and (4) Violation Type due to the constraints of the database.
#
# Both SIN numbers, Vehicle Serial No, and Violation type must match pre-entered 
# data in the database. 

#---------------------------------------------------------------------------------
# iii.a. Driver Search
#---------------------------------------------------------------------------------
# Driver search allows the user to specify a name or Sin. The user parameter is then
# used to query the drive_licence table for matching names/licence numbers. If the
# name is found all relevant licence information is displayed. If the name is found
# in people table but the person is not in the drive_licence table 
# their licence #  is displayed with an N/A to indicate the lack of a licence.
# 
# i. The user can specify the way to search by tabbing into the "search by name/search 
# by licence number" and pressing enter on the field.  
# 
# ii. The user can scroll through the results by tabbing into the the results field
# and using the arrow keys to scroll through the results.
# 
# The search will display:
# (1) Name, (2) Licence no, (3) Addresss, (4) Birthday, (5) Licence class, (6) Conditions,
# (7) Expiring Date
# 

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

#---------------------------------------------------------------------------------
# iv. General Interface Information
#---------------------------------------------------------------------------------
#
# i. Note: For Date Type information, you are able to set them as 'unset' in the
# interface. However to maintain consistant error checking for database input (for 
# proper processing when you enter a DATE type value into Oracle) we will have 
# 'unset' set to today's date instead of an empty string.
#
# For the driver licence modules, the default 'unset' values are slightly different.
# Please refer to that section for further detail.
#
# ii. Before you can interact with the module, you must log into an ORACLE SERVER.
# The default server is set to the c291 student access given in lab. The user 
# must log in or else an error will prompt them to log in.






