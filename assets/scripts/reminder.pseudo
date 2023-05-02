def get_user_input(input_str):
    return 0

def display_options(input_str):
    return 0

def load_meetings():
    return 0

def update_meeting( meeting_number ):
    meeting_to_update = this.meetings[ 'meeting_number' ]
    user_options = { '1': "Add Participant", "2": "Update Time", "3":"Toggle Notifications On/Off", 'D':"Delete Meeting"}
    display_options( user_options)
    # if valid then continue , otherwise break and restart loop 
    while 1:
        opt = get_user_input(user_options) 
        # if valid then continue , otherwise break and restart loop 
        if opt is valid and 1 : 
            meeting_to_update.add_new_participant()
        if opt is valid and 2 : 
            meeting_to_update.update_time()
        if opt is valid and 3: 
            meeting_to_update.toggle_notifications()
        if opt is valid and 'D': 
            this.delete_meeting( meeting_to_update )

    this.update_worksheept('meetings')
    return 0

def manage_meetings():
    # load meetings from worsheet 
    this.load_data_from_cloud('meetings')
    user_options = 'use dict comprehenesion to create a dict using data from the meetings object'; 
    # add another optiom : 
    #  "C : Create Meetings" 
    #  "B : Back to Previous Screen" 
    display_options( user_options)
     # if valid then continue , otherwise break and restart loop 
    while 1:
        opt = get_user_input(user_options) 
        # if valid then continue , otherwise break and restart loop 
        if opt is valid and is_a_number : 
            update_meeting( opt )
        if opt is valid and 'C' : 
            create_new_meeting()
        if opt is valid and 'B' : 
            return 0 
    return 0

def create_new_meeting():
    return 0    

def main():
    clear_screen()
    user_options = { '1': "Manage Meetings", "2": "Create New Meeting"}
    display_options( user_options)
    while 1:
        opt = get_user_input(user_options) 
        # if valid then continue , otherwise break and restart loop 
        if opt is valid and 1 : 
            manage_meetings()
        if opt is valid and 2 : 
            create_new_meeting()

