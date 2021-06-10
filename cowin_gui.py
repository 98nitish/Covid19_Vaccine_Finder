# %%
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Style
import cowin
import time
import threading
# %%
window = Tk()
window.geometry('400x300')
window.resizable(0, 0)
window.title('COVID19 Vaccine Finder')
# %%
# function to fetch the list of states and preview it in combobox 
# and if any of the state is selected from the combobox it calls the get_district function
def get_state():
    for frame in window.winfo_children():
        frame.destroy()
    global frame1
    frame1 = Frame(window).place()
    global selected_state
    print('Selected', search_by.get())
    label = Label(frame1, text = 'Select State: ', foreground = 'black').place(x = 45, y = 90)
    cowin.get_states()
    selected_state = StringVar()
    states = Combobox(frame1, textvariable = selected_state, foreground = 'black')
    states['values'] = cowin.state_df['state_name'].to_list()
    states.place(x = 145, y = 90)
    states.bind('<<ComboboxSelected>>', get_district)
# %%
# function to fetch the district for the particular state selected in get_state function
# used to search for sessions using district
def get_district(event):
    global selected_district
    print('Selected', selected_state.get())
    label = Label(frame1, text = 'Select District: ', foreground = 'black').place(x = 45, y = 140)
    state_filt = cowin.state_df['state_name'] == selected_state.get()
    state_id = int(cowin.state_df.loc[state_filt, 'state_id'])
    cowin.get_district(state_id)
    selected_district = StringVar()
    districts = Combobox(frame1, textvariable = selected_district, foreground = 'black')
    districts['values'] = cowin.district_df['district_name'].to_list()
    districts.place(x = 145, y = 140)
    districts.current(0)
    button_home = Button(frame1, text = 'Home', command = home, foreground = 'black').place(x = 110, y = 190)
    state_search = Button(frame1, text = 'Search', command = get_sessions, foreground = 'black').place(x = 210, y = 190)
# %%
# function to find session using pincode that is manually entered by the user in an entry widget
def pin_search():
    for frame in window.winfo_children():
        frame.destroy()
    frame1 = Frame(window).place()
    global pincode
    print('Selected', search_by.get())
    label = Label(frame1, text = 'Enter Pincode: ', foreground = 'black').place(x = 45, y = 100)
    pincode = StringVar()
    entry = Entry(frame1, textvariable = pincode, foreground = 'black', background = 'grey').place(x = 145, y = 100)
    button_home = Button(frame1, text = 'Home', command = home, foreground = 'black').place(x = 110, y = 150)
    button_search = Button(frame1, text = 'Search', command = get_sessions, foreground = 'black').place(x = 210, y = 150)
# %%
# check for entering correct pincode
def pincode_warning():
    no_pincode_warning = messagebox.showwarning('Mandatory Field', 'Please enter correct Pincode.')
# %%
# getting the sesssion either by using pincode or district whichever the user selected
# it calls the function in cowin module to get the session
def get_sessions():
    # flag ensures that frame only changes if the inputs are validated
    flag = False
    global pincode
    if(search_by.get() == 'Pincode'):
        if(len(pincode.get()) == 6):
            try:
                cowin.search_by_pincode(int(pincode.get()))
                flag = True
            except:
                pincode_warning()
        else:
            pincode_warning()
    else:
        print('Selected', selected_district.get())
        district_filt = cowin.district_df['district_name'] == selected_district.get()
        district_id = int(cowin.district_df.loc[district_filt, 'district_id'])
        cowin.search_by_district(district_id)
        flag = True
    if(flag):
        for frame in window.winfo_children():
            frame.destroy()
        frame1 = Frame(window).place()
        cowin.get_appointment()
        if(cowin.appointment_df.empty):
            label = Label(frame1, text = 'No place found in this Pincode 🥺', foreground = 'black').place(x = 85, y = 100)
            button_home = Button(frame1, text = 'Home', command = home, foreground = 'black').place(x = 160, y = 150)
        else:
            filter_vaccine()
# %%
# getting filter variables from the user using combobox
def filter_vaccine():
    global dose_type, min_age, vaccine, fee_type
    for frame in window.winfo_children():
        frame.destroy()
    frame1 = Frame(window).place()

    label = Label(frame1, text = 'Lets apply some filters to get preferred type vaccine. 🙄', foreground = 'black').place(x = 25, y = 10)

    # Filtering Dose Type (Dose 1 or Dose 2)
    label = Label(frame1, text = 'Select Vaccine Dose: ', foreground = 'black').place(x = 25, y = 60)
    dose_type = StringVar()
    dose_types = Combobox(frame1, textvariable = dose_type, foreground = 'black')
    dose_types['values'] = ['Dose 1', 'Dose 2']
    dose_types.place(x = 165, y = 60)
    dose_types.current(0)

    # Filtering Min_Age (18+ or 45+)
    label = Label(frame1, text = 'Select Min Age: ', foreground = 'black').place(x = 25, y = 110)
    min_age = IntVar()
    min_ages = Combobox(frame1, textvariable = min_age, foreground = 'black')
    ages = list(cowin.appointment_df['min_age_limit'].unique())
    ages.sort()
    min_ages['values'] = ages
    min_ages.place(x = 165, y = 110)
    min_ages.current(0)

    # Filtering Vaccine (Covidshield or Covaxin)
    label = Label(frame1, text = 'Select Vaccine: ', foreground = 'black').place(x = 25, y = 160)
    vaccine = StringVar()
    vaccines = Combobox(frame1, textvariable = vaccine, foreground = 'black')
    vaccine_list = list(cowin.appointment_df['vaccine'].unique())
    vaccine_list.append('Any')
    vaccine_list.sort()
    vaccines['values'] = vaccine_list
    vaccines.place(x = 165, y = 160)
    vaccines.current(0)

    # Filtering Cost (Free or Paid)
    label = Label(frame1, text = 'Select Price Variant: ', foreground = 'black').place(x = 25, y = 210)
    fee_type = StringVar()
    fee_types = Combobox(frame1, textvariable = fee_type, foreground = 'black')
    fee_types['values'] = ['Any', 'Free', 'Paid']
    fee_types.place(x = 165, y = 210)
    fee_types.current(0)

    button_home = Button(frame1, text = 'Home', command = home, foreground = 'black').place(x = 60, y = 260)
    button_filters = Button(frame1, text = 'Apply filters and search', command = filters, foreground = 'black').place(x = 160, y = 260)
# %%
# function to prompt warning while closing the program
def close_warning():
    warning_message = messagebox.askyesno('Quit Search', 'Are you sure you want to quit the search?', icon = 'warning')
    if(warning_message):
        window.destroy()
# %%
# applying filter and creating thread for continuous search
def filters():
    for frame in window.winfo_children():
        frame.destroy()
    frame1 = Frame(window).place()

    if(vaccine.get() == 'Any'):
        available_vaccine = list(cowin.appointment_df['vaccine'].unique())
    else:
        available_vaccine = [vaccine.get()]

    if(fee_type.get() == 'Any'):
        cost = ['Free', 'Paid']
    else:
        cost = [fee_type.get()]

    # creating filter variable with all those filters which were taken as input from user
    global filt, dose
    dose_type_dict = {'Dose 1' : 'available_capacity_dose1', 'Dose 2' : 'available_capacity_dose2'}
    dose = dose_type_dict[dose_type.get()]
    filt = (cowin.appointment_df[dose] > 0)\
        & (cowin.appointment_df['min_age_limit'] == min_age.get())\
            & (cowin.appointment_df['fee_type'].isin(cost))\
                & (cowin.appointment_df['vaccine'].isin(available_vaccine))

    label = Label(frame1, text = 'Searching Vaccine Stay Tuned 😁', foreground = 'black').place(x = 100, y = 100)
    button_stop = Button(frame1, text = 'Stop', command = close_warning, foreground = 'black').place(x = 170, y = 150)
    # creating thread and setting it as daemon so the thread gets killed once the main process is closed
    t1 = threading.Thread(target = continous_search)
    t1.daemon = True
    t1.start()
# %%
# function to format and pass each row of available_appointment df
def display_result(df_row):
    df_row['slots'] = ('\n').join(df_row['slots'])
    tree.insert('', 'end', values = (df_row['date'], df_row['name'], df_row[dose], df_row['slots'], df_row['vaccine'], df_row['address'], df_row['cost']))
# %%
# function to display final output once slots are found
def slots_found():
    global tree
    for frame in window.winfo_children():
        frame.destroy()
    window.geometry('1200x550')
    slots_found_message = messagebox.showinfo('Slots Found', 'Slots are available according to your filters.')
    tree = Treeview(window, columns = ('Date','Name', 'Available_capacity', 'Slots', 'Vaccine', 'Address', 'Cost'))
    tree.heading('Date', text = 'Date')
    tree.heading('Name', text = 'Name')
    tree.heading('Available_capacity', text = 'Available Capacity')
    tree.heading('Slots', text = 'Slots')
    tree.heading('Vaccine', text = 'Vaccine')
    tree.heading('Address', text = 'Address')
    tree.heading('Cost', text = 'Cost')
    tree.column('Date', width = 90)
    tree.column('Name', width = 250)
    tree.column('Available_capacity', width = 110)
    tree.column('Slots', width = 130)
    tree.column('Vaccine', width = 100)
    tree.column('Address', width = 480)
    tree.column('Cost', width = 40)
    tree['show'] = 'headings'
    style = Style()
    style.configure('Treeview.Heading', foreground = 'black', background = 'white', fieldbackground = 'white')
    style.configure('Treeview', foreground = 'black', background = 'white', fieldbackground = 'white', rowheight = 75)
    final_appointmnet_df = available_appointment.sort_values(by = 'date')
    final_appointmnet_df.apply(display_result, axis = 1)
    tree.pack()
# %%
# function that keeps on fetching the data and searching if there is a match according to the filter.
# the data is fetched in every 15 mins if there is no match 
def continous_search():
    global available_appointment
    while(True):
        available_appointment = cowin.appointment_df.loc[filt]
        # checking if there is a match
        if(not available_appointment.empty):
            print('Found a slot 👍')
            slots_found()
            break

        print('No slots found, will try again after 5 mins. 👎')
        time.sleep(5 * 60)
        cowin.get_appointment()
# %%
#  creating the home interface
def home():
    global search_by
    for frame in window.winfo_children():
        frame.destroy()
    frame1 = Frame(window).place()
    search_by = StringVar()
    label = Label(frame1, text = 'Search by: ', foreground = 'black').place(x = 130, y = 100)
    pin_radio = Radiobutton(frame1, text = 'Pincode', value = 'Pincode', variable = search_by, foreground = 'black', tristatevalue = 0,command = pin_search).place(x = 200, y = 120)
    district_radio = Radiobutton(frame1, text = 'District', value = 'District', variable = search_by, foreground = 'black', tristatevalue = 0, command = get_state).place(x = 200, y = 150)
# %%
home()
# %%
# close button calls close_warning function
window.protocol('WM_DELETE_WINDOW', close_warning)
# %%
window.mainloop()
# %%
