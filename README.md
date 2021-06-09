# Covid19_Vaccine_Finder
The application is based on Tkinter in Python and is used to find vaccine for Covid19 in India using Cowin API.

The user needs to run the cowin_gui.py file using Python.
Once that a GUI based application will start and the user can follow the instruction to find the vaccine slot.
The options that the user get are: 
- Search By (PIN or District)
- Depending on the selection either enter PIN or select District from drop down menu.
- After step 2, the user needs to apply filters for the vaccine (like vaccines type, cost, min age, dose type)
- Once the filters are applied the application starts the search for the vaccine which the user chose.
  - If the vaccine is found the user gets a prompt that slots are found and displays the details.
  - If there is no slots for the vaccine the user selected, the application keeps on searching for the slots every 15 mins until a slot is found or the user terminates the program.
