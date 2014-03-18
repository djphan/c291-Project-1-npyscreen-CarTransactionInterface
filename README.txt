cmput-291-project-1
===================

CMPUT 291 Project 1 (Python 3)

__________________________
COMMUNICATION / NOTES     |
__________________________|
Dan: The due date got pushed back to Friday 6:00 PM (in case things come up) but lets finish early.
https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=329146

!!! Test cases are up:
https://eclass.srv.ualberta.ca/mod/page/view.php?id=998610
We will have to alter some things to comply with these new requirements. Nothing too major though.

 	driver_search.py            <--- done
 	vehicle_history_search.py   <- Dan
 	violation_search.py         <--- Jon (near completion)
 	
If you want to work on one of them please make a note here so we don't end up doing the same thing twice.

Other TO-DO's:
  Finish error checking/validation for:
    ViolationRecord     <--} Dan: Primary key Updated. Can either of you use your database to test for additional
                             Cases. Will double check date a little later.
                           } will add people form where needed  
    AutoTransaction     <--} once it's ready - Carl
    
    DriverLicence       <-- Jon will finish Monday with TA(BLOB issue)
    NewVehicleRegistration?? (at least mostly done) <-- Jon (near completion)
    Create add_people form            <-- Jon 

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
#     ii.a.
#     ii.b.
#     ii.c. 
#     ii.d. Violation Record
# iii. Search
#     iii.a.
#     iii.b.
#     iii.c.
#---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------
# ii.d. Violation Record
#---------------------------------------------------------------------------------

Violation record will allow the user to enter data into the ticket table. 
i. The basic form will allow the officer to input any driver they pull over to record
the ticket. 

ii. If the officer does not know the Violator SIN, he is able to pull up
the primary owner of the vehicle in question using the 'Use Vehicle's Primary Owner SIN'
button. This will query the database to obtain, and autofill the Violator SIN field with
the primary owner's SIN. The Violator SIN field will be overrode if this option is used
if there were any previous values entered into the field.

The following fields are required: (1) Violator SIN (2) Vehicle Serial No 
(3) Officer SIN and (4) Violation Type due to the constraints of the database.

Both SIN numbers, Vehicle Serial No, and Violation type must match pre-entered 
data in the database. 




