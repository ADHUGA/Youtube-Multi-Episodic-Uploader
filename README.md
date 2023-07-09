# Youtube-Multi-Episodic-Uploader
A program that utilizes YoutTube Data v3 to automate multi-part videos such as walkthroughs and episodes


YOU NEED TO CREATE A CRED.PY FILE THAT HAS:
-------------------------------------------
API_KEY=""

credentials=""
-------------------------------------------
The API_Key = "(your key here)" can be acquired at https://console.cloud.google.com/apis/library/youtube.googleapis.com
  When you have made a project, go to the credentials page and get your API key there.
  
The credentials can also be found at the same place. Under credentials you can create an oauth key for a desktop application.
  Once that is done download the json and input the file location download of that file as a string (ie. C:\\Users\\yourname\\....\(json file))
  
IMPORTANT NOTES WHEN USING THIS PROGRAM:
  

Your videos titles need to use the format of "Title #(number here)". 

The title needs a # and the thumbnails folder needs the number corresponding in the title of #.jpg

Also convert your time appropriately and try not to upload too close to the current time.

Lastly, make sure your video is not too long (around 10-15 minutes is good).



A video of using this can be found here: https://www.youtube.com/watch?v=TVYzIwhLj4A
