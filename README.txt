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

TO DO:
 	driver_search.py            <--- done
 	vehicle_history_search.py   <- Dan
 	violation_search.py         <--- Jon (near completion)
 	
If you want to work on one of them please make a note here so we don't end up doing the same thing twice.

Other TO-DO's:
  Finish error checking/validation for:
    ViolationRecord
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


