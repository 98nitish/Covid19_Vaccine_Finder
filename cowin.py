# %%
import requests
import pandas as pd
from datetime import datetime, timedelta
# %%
# creating header to portray as a browser
head = {
'user-agent': 'Safari/14.1',
}
# %%
server = 'https://cdn-api.co-vin.in/api/'
url_appointment = ''
# %%
# function to get the list of states
def get_states():
    global state_df
    url_states = server + 'v2/admin/location/states'
    state_response = requests.get(url_states, headers = head)
    assert (state_response), 'Error in getting State List 👎'
    print('Got State List 👍')
    state_list = state_response.json()['states']
    state_df = pd.DataFrame(state_list)

# function to get the list of districts of the selected state
# selected state is known by state_id which is passed as a parameter
def get_district(state_id):
    global district_df
    url_districts = server + 'v2/admin/location/districts/' + str(state_id)
    district_response = requests.get(url_districts, headers = head)
    assert (district_response), 'Error in Getting District List 👎'
    print('Got District List 👍')
    district_list = district_response.json()['districts']
    district_df = pd.DataFrame(district_list)

# creating the url to fetch sessions using district_id
def search_by_district(district_id):
    global url_appointment
    url_appointment = server + 'v2/appointment/sessions/public/calendarByDistrict?district_id='\
                        + str(district_id) + '&date='
# %%
# function to create url to fetch session using pincode input given by the user
def search_by_pincode(pincode):
    global url_appointment
    pin = str(pincode)
    url_appointment = server + 'v2/appointment/sessions/public/calendarByPin?pincode='\
                        + pin + '&date='
# %%
# creates a dataframe appointment_df with all the required details to be displayed
def final_sessions(df_row):
    global appointment_df
    df_row.fillna(0, inplace = True)
    if(df_row['fee_type']  == 'Free'):
        cost = str(0)
    else:
        cost = df_row['vaccine_fees'][0]['fee']
    sessions = pd.DataFrame(df_row['sessions'])
    sessions.drop(['session_id', 'available_capacity'], axis = 1, inplace = True)
    sessions['name'] = df_row['name']
    address_old_format = df_row['address']
    if(len(address_old_format) > 65):
        first_space = address_old_format.find(' ', 55, 65)
        address_new_format = address_old_format[ : first_space]
        address_new_format += '\n'
        address_new_format += address_old_format[first_space + 1 : ]
    else:
        address_new_format = address_old_format
    sessions['address'] = address_new_format
    sessions['fee_type'] = df_row['fee_type']
    sessions['cost'] = cost
    appointment_df = appointment_df.append(sessions)
# %%
# function to get sessions using the url created by search_by_pincode function or search_by_district function
def appointment(date):
    global centers_df
    final_url = url_appointment + date
    appointment_response = requests.get(final_url, headers = head)
    assert (appointment_response), 'Error in getting session details 👎'
    print('Got Sessions Details 👍')
    centers_list = appointment_response.json()['centers']
    centers_df = pd.DataFrame(centers_list)
    if(not centers_df.empty):
        centers_df.apply(final_sessions, axis = 1)
# %%
# function to get sessions for 2 weeks (default cowin sends 1 week data)
def get_appointment():
    global url_appointment, appointment_df
    # getting the current date and formating it as required to call the API
    current_datetime = datetime.now()
    date = current_datetime.strftime('%d-%m-%Y')
    appointment_df = pd.DataFrame()
    appointment(date)
    if(not centers_df.empty):
        # adding 7 days to the current date to fetch next week data
        print('Getting second week data 🙂')
        date = (current_datetime + timedelta(days = 7)).strftime('%d-%m-%Y')
        appointment(date)
# %%