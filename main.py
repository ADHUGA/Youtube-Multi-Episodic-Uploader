import json
import os
import tkinter as tk
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from googleapiclient.http import MediaFileUpload
from tkcalendar import Calendar
from tktimepicker import *
from datetime import datetime
from tkinter import ttk
from datetime import datetime, time, timedelta
from googleapiclient.errors import HttpError
from datetime import date
import creds
import re

# Load the client credentials from JSON file
credentials_file = creds.credentials_file
scopes = ["https://www.googleapis.com/auth/youtube"]
flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
credentials = flow.run_local_server(port=8080)
API_KEY = creds.API_KEY

#TO-DO Potential AI Generation of Title and Description
#Gaming Title Could be Added

global_video_title = ""
global_video_description = ""
global_video_tags = []
global_video_category_id = ""
currentNumber = ""
base_title = ""
video_folder_path = ""
thumbnail_folder_path = ""

global_selected_date = None
global_selected_time = None

ISO_time = "" #Is a string

# def print_mess():
#     global ISO_time
#     print("These are your global values:")
#     print("Your global_video_title  is: " + global_video_title)
#     print("Your global_video_description is: " + global_video_description)
#     print("Your global_video_tags is: " + str(global_video_tags))
#     print("Your global_video_category_id is: " + global_video_category_id)
#     print("Your currentNumber is: " + currentNumber)
#     print("Your base_title is: " + base_title)
#     print("Your video_folder_path is: " + video_folder_path)
#     print("Your thumbnail_folder_path is: " + thumbnail_folder_path)
#     print("Your global_increment is (to string) : " + str(global_increment))
#     print("Your global_selected_date (to string) is: " + str(global_selected_date))
#     print("Your global_selected_time (to string) is: " + str(global_selected_time))
#     # date = datetime.strptime(global_selected_date, "%m/%d/%y")
#     # time = datetime.strptime(global_selected_time, "%H:%M").time()
#     # combined_time = datetime.combine(date, time)
#     # ISO_time = combined_time.isoformat()
#     variable_type = type(ISO_time)
#     print(variable_type)
#     print("Your ISO_time is " + str(ISO_time))
#     variable_type = type(ISO_time)
#     print(variable_type)
#     print("My ISO_time is " + str(variable_type) + " After I did str()")



def select_folder1():
    global video_folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        mp4_files = [file for file in os.listdir(folder_path) if file.endswith(".mp4")]
        # Do something with the selected folder path
        print("Selected Video Location:", folder_path)
        print("MP4 files found:")
        for file in mp4_files:
            print(file)

        video_folder_path = folder_path
        folder_label.config(text="Chosen Location of Videos: " + folder_path)
        return mp4_files


def select_folder2():
    global thumbnail_folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Retrieve all file names in the folder
        file_names = os.listdir(folder_path)

        # Filter file names with ".jpg" extension
        jpg_files = [file for file in file_names if file.lower().endswith(".jpg")]

        # Print the selected jpg files
        for jpg_file in jpg_files:
            print("Selected JPG File:", os.path.join(folder_path, jpg_file))

        thumbnail_folder_path = folder_path
        thumbnail_label.config(text="Chosen Location of Thumbnails: " + folder_path)
        return jpg_files




def search_video():
    global global_video_title, global_video_description, global_video_tags, global_video_category_id, currentNumber, base_title

    video_title = search_entry.get()

    # Get the channel ID for your own YouTube channel
    channels_response = youtube.channels().list(
        part='id',
        mine=True
    ).execute()

    if 'items' in channels_response:
        channel_id = channels_response['items'][0]['id']

        # Perform the YouTube API search to get a list of video IDs from your own channel
        search_response = youtube.search().list(
            part='id',
            q=video_title,
            maxResults=1,
            channelId=channel_id
        ).execute()

        if 'items' in search_response:
            video_id = search_response['items'][0]['id']['videoId']

            # Retrieve the video metadata using the video ID
            videos_response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            if 'items' in videos_response:
                video = videos_response['items'][0]
                global_video_title = video['snippet']['title']
                global_video_description = video['snippet']['description']
                if 'tags' in video['snippet']:
                    global_video_tags = video['snippet']['tags']
                else:
                    global_video_tags = []  # Set an empty list if 'tags' field is not present

                try:
                    global_video_category_id = video['snippet']['categoryId']
                except KeyError:
                    global_video_category_id = "Unknown"  # Provide a default value when 'categoryId' key is not present

                # Print the retrieved metadata for testing
                print("Video Title:", global_video_title)
                print("Video Description:", global_video_description)
                print("Video Tags:", global_video_tags)
                print("Video Category ID:", global_video_category_id)

                # # Update the result labels with the retrieved information
                # label_video_title.config(text="Video Title: " + global_video_title)
                # label_video_description.config(text="Video Description: " + global_video_description)
                # label_video_tags.config(text="Video Tags: " + ", ".join(global_video_tags))
                # label_video_category_id.config(text="Video Category ID: " + global_video_category_id)

                # Other actions you may want to perform using the metadata

                # Parse the video title and extract the number after the "#"
                match = re.search(r"#(\d+)", global_video_title)
                if match:
                    video_number = match.group(1)
                    # Use the extracted video number as needed
                    print("Video Number:", video_number)
                    currentNumber = video_number

                # Separate the title by removing everything after the "#"
                    # Separate the title by removing everything after the "#"
                    separate_title = global_video_title.split("#")[0].strip()
                    base_title = separate_title + " #"
                    print("Separate Title:", base_title)

                # Update the Boolean variable based on the search result
                accepted_label.config(text="Accepted Video Found", fg="green")
            else:
                # If no video found, display an error message
                accepted_label.config(text="Error: No Video Found", fg="red")
                label_error.config(text="No video found with the provided title.")
        else:
            # If no video found, display an error message
            accepted_label.config(text="Error: No Video Found", fg="red")
            label_error.config(text="No video found with the provided title.")
    else:
        # If no channel found, display an error message
        accepted_label.config(text="Error: No Channel Found", fg="red")
        label_error.config(text="No channel found for your account.")






def upload_video():
    global video_folder_path, thumbnail_folder_path, currentNumber, base_title, global_video_tags, global_video_category_id, global_video_description, global_video_tags, global_selected_time, global_selected_date, ISO_time, API_KEY

    video_metadata = {
        'snippet': {
            'title': 'My Video Title',
            'description': 'My Video Description',
            'tags': ['tag1', 'tag2', 'tag3'],
            'categoryId': '22'  # Replace with the appropriate category ID
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': ISO_time
        }
    }

    #print("Got past global")

    if video_folder_path == "": #Makes sure user hits the video button first
        print("Please select the video folder path")
        return

    if thumbnail_folder_path == "": #Makes sure user hits the thumbnail button first
        print("Please select the thumbnail folder path")
        return

    video_files = os.listdir(video_folder_path)
    mp4_files = [file for file in video_files if file.endswith(".mp4")]

    for mp4_file in mp4_files:

        #JUST ADDED THIS TAKE OUT IF BREAKS. THE DAY WAS NOT INCREMENTING!
        video_metadata = {
            'snippet': {
                'title': 'My Video Title',
                'description': 'My Video Description',
                'tags': ['tag1', 'tag2', 'tag3'],
                'categoryId': '22'  # Replace with the appropriate category ID
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': ISO_time
            }
        }

        currentNumber = int(currentNumber) + 1
        currentNumber = str(currentNumber)
        video_path = os.path.join(video_folder_path, mp4_file)
        thumbnail_file = f"{currentNumber}.jpg"
        thumbnail_path = os.path.join(thumbnail_folder_path, thumbnail_file)

        # Create a MediaFileUpload object for the video
        video_body = MediaFileUpload(video_path)

        # Create a MediaFileUpload object for the thumbnail
        thumbnail_body = MediaFileUpload(thumbnail_path)

        # Set the video title based on the base title and current number
        video_metadata['snippet']['title'] = f"{base_title}{currentNumber}"
        video_metadata['snippet']['description'] = global_video_description
        video_metadata['snippet']['tags'] = global_video_tags
        video_metadata['snippet']['categoryId'] = global_video_category_id
        # Need to Sets other parts here too.

        try:
            # Perform the video upload
            request = youtube.videos().insert(
                part='snippet,status',
                body=video_metadata,
                media_body=video_body
            )
            response = request.execute()

            # Print the video upload response
            print("Video Upload Response:", response)

            if 'id' in response:
                video_id = response['id']

                # Set the thumbnail for the video
                thumbnail_response = youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=thumbnail_body
                ).execute()

                # Print the thumbnail upload response
                print("Thumbnail Upload Response:", thumbnail_response)
            datetime_obj = datetime.fromisoformat(ISO_time)
            next_day = datetime_obj + timedelta(days=global_increment)
            next_day_ISO_time = next_day.isoformat()
            ISO_time = next_day_ISO_time
                #time.sleep(10)

                #Schedule
                # print("This is my ISO " + ISO_time)
                # publish_at = datetime.fromisoformat(ISO_time).isoformat() #Makes sure it is in ISO Format
                # print("This is my publish_at " + publish_at)
                # publish_request = youtube.videos().update(
                #     part='status',
                #     body={'id': video_id, 'status': {'publishAt': publish_at}},
                #     key=API_KEY
                # )
                # publish_response = publish_request.execute()
                # print("Video uploaded successfully!")
                # datetime_obj = datetime.fromisoformat(ISO_time)
                # next_day = datetime_obj + timedelta(days=global_increment)
                # next_day_ISO_time = next_day.isoformat()
                # ISO_time = next_day_ISO_time
        except HttpError as e:
            print("An HTTP error occurred during the video upload:", e)
            return


def set_increment(value):
    global global_increment
    if value == 1:
        global_increment = 1
    elif value == 7:
        global_increment = 7


def select_date():
    global global_selected_date, global_increment, ISO_time
    top = tk.Toplevel(window)
    top.title("Select Date")

    def on_date_selected():
        global global_selected_date, ISO_time
        selected_date = cal.get_date()
        date_label.config(text="Selected Date is: " + selected_date) #Shown once selected
        global_selected_date = selected_date
        try:
            date = datetime.strptime(global_selected_date, "%m/%d/%y")
            time = datetime.strptime(global_selected_time, "%H:%M").time()
            combined_time = datetime.combine(date, time)
            ISO_time = combined_time.isoformat()
        except:
            print("Now select the time.")
        top.destroy()

    today = date.today()
    cal = Calendar(top, selectmode='day', mindate=today)
    cal.pack(pady=20)

    button = tk.Button(top, text="Select Date", command=on_date_selected)
    button.pack(pady=10)



    # if selected_option.get() == "24h":
    #     increment_value = 1
    #     global_increment = increment_value
    # elif selected_option.get() == "1w":
    #     increment_value = 7
    #     global_increment = increment_value


def select_time():
    global global_selected_time, global_increment, ISO_time
    def on_time_selected():
        global global_selected_time, ISO_time
        selected_time = time_picker.get()
        time_label.config(text="Selected Time is: " + selected_time)
        global_selected_time = selected_time
        try:
            date = datetime.strptime(global_selected_date, "%m/%d/%y")
            time = datetime.strptime(global_selected_time, "%H:%M").time()
            combined_time = datetime.combine(date, time)
            ISO_time = combined_time.isoformat()
        except:
            print("Now select the date.")
        top.destroy()

    top = tk.Toplevel(window)
    top.title("Select Time")

    # Generate a list of time values in 15-minute increments throughout the day
    time_values = []
    for hour in range(24):
        for minute in range(0, 60, 15):
            time_str = f"{hour:02d}:{minute:02d}"
            time_values.append(time_str)

    time_picker = ttk.Combobox(top, values=time_values, state="readonly")
    time_picker.pack(pady=20)

    button = tk.Button(top, text="Select Time", command=on_time_selected)
    button.pack(pady=10)

    # if selected_option.get() == "24h":
    #     increment_value = 1
    #     global_increment = increment_value
    # elif selected_option.get() == "1w":
    #     increment_value = 7
    #     global_increment = increment_value


# Build the API client
youtube = build('youtube', 'v3', credentials=credentials)


# Create the GUI window
window = tk.Tk()
window.title("YouTube Multi Episodic Uploader")
window.geometry("1024x868")

global_increment = None

selected_value = tk.IntVar()


# Create the left pane
left_pane = tk.Frame(window)
left_pane.grid(row=0, column=0, padx=80, pady=60)



# Create the "Enter Title of First Video" label
title_label = tk.Label(left_pane, text="Enter Title of Most Recent Video of Series:")
title_label.grid(row=0, column=0, padx=10, pady=10)

# Create the search entry
search_entry = tk.Entry(left_pane, width=50)
search_entry.grid(row=1, column=0, padx=10, pady=10)

# Create the search button
search_button = tk.Button(left_pane, width=20, text="Search", command=search_video)
search_button.grid(row=2, column=0, padx=10, pady=10)

#Create the folder options
button1 = tk.Button(left_pane, text="Select folder where your videos to upload are stored!", command=select_folder1)
button1.grid(row=3, column=0, padx=10, pady=80)
button2 = tk.Button(left_pane, text="Select folder where your corresponding thumbnails are!", command=select_folder2)
button2.grid(row=4, column=0, padx=10, pady=30)

#Create option for 24 hours left pane
option_24h = tk.Radiobutton(left_pane, text="24 hours", variable=selected_value, value=1, command=lambda: set_increment(selected_value.get()))
option_24h.grid(row=9, column=0, padx=10, pady=30)





# Create the upload button
upload_button = tk.Button(left_pane, width=20, text="Begin Upload", command=upload_video)
upload_button.grid(row=10, column=0, padx=10, pady=10)


# Create the "Selected Date" label






# Create the right pane
right_pane = tk.Frame(window)
right_pane.grid(row=0, column=1, padx=80, pady=60)

# Displays if video is Found
accepted_label = tk.Label(left_pane, text="", font=("Arial", 12, "bold"))
accepted_label.grid(row=1, column=1, padx=30, pady=10)

# Displays Location of Videos
folder_label = tk.Label(left_pane, text="Chosen Location of Videos: ")
folder_label.grid(row=3, column=1, padx=30, pady=10)

# Displays Location of Thumbnails
thumbnail_label = tk.Label(left_pane, text="Chosen Location of Thumbnails: ")
thumbnail_label.grid(row=4, column=1, padx=30, pady=30)


# Create the option for a week later
option_1w = tk.Radiobutton(left_pane, text="A week later", variable=selected_value, value=7, command=lambda: set_increment(selected_value.get()))
option_1w.grid(row=9, column=1, padx=30, pady=30)






# Create the "When do you want the next video uploaded?" label
upload_label = tk.Label(left_pane, text="Schedule the upload date for the first video: ")
upload_label.grid(row=5, column=0, padx=30, pady=10, sticky="e")

# Create a frame inside the right pane
date_frame = tk.Frame(right_pane)
date_frame.grid(row=5, column=0, padx=10, pady=10)



#Calendar
date_label = tk.Label(left_pane, text="Selected Date is: ") #Actually shown on GUI
date_label.grid(row=6, column=1, padx=10, pady=10)

# Creates the "Date" button within the program
date_button = tk.Button(left_pane, text="Date", command=select_date)
date_button.grid(row=6, column=0, padx=10, pady=10)

#Time
time_label = tk.Label(left_pane, text="Selected Time is: ")
time_label.grid(row=7, column=1, padx=10, pady=10)

# Creates the "Date" button within the program
time_button = tk.Button(left_pane, text="Time", command=select_time)
time_button.grid(row=7, column=0, padx=10, pady=10)

#Next Video Label
next_label = tk.Label(left_pane, text="When should the next video be uploaded?")
next_label.grid(row=8, column=0, padx=30, pady=10, sticky="e")

# cringe_button = tk.Button(left_pane, text="Cringe", command=print_mess)
# cringe_button.grid(row=11, column=0, padx=30, pady=10, sticky="e")




# Start the GUI main loop
window.mainloop()


