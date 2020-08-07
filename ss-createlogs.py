# Created by Olly and Mason 

import json
import os
import argparse
from datetime import datetime

class Message:
    def __init__(self, user, message, timestamp):
        self.user = user
        self.message = message.replace("\u00e2\u0080\u0099", "'")\
                                .replace("&lt;", "<")\
                                .replace("&gt;", ">")
        self.timestamp = timestamp

class MessageEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class File:
    def writelogfile():
        print("Creating your log file now. This may take a while...")
        # this process searches the log directory for log "files"
        # each folder represents a channel that was created on a slack team
        # in each folder there is a json file containing chat logs for each day
        # the process iterates through each folder, reads the file,
        # extracts the data we want and appends is to the array
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file not in ignored_files:
                    with open(subdir + "/" + file, "r", encoding="Latin1") as json_file:
                        data = json.load(json_file)
                        for text in data:

                            if (text['type'] != "message"):
                                continue
                            if ("subtype" in text):
                                continue
                            if ("files" in text):
                                continue
                            if ("user_profile" not in text):
                                continue

                            msg_text = text['text']
                            msg_user = text['user_profile']['display_name']
                            # convert unix time stamp to a readable format
                            msg_ts = datetime.utcfromtimestamp(int(float(text['ts']))).strftime('%Y-%m-%d %H:%M:%S')

                            msg = Message(msg_user, msg_text, msg_ts)
                            messages.append(msg)
                            
                else:
                    continue

        # create a file and write the data in the array in to a json format
        # this file contains every message with the junk stripped out
        # the file will then be used for data analysis.
        with open("master_log.json", "w") as outfile:
            data = json.dumps(messages, indent=4, cls=MessageEncoder)
            outfile.write(data)
            print("Chat log successfully dumped.")
    

# create a parser for the program
parser = argparse.ArgumentParser(prog='Slack Stats', description='Find out interesting stats about your slack team!')

# optional flag to print version
parser.add_argument('--version', action='version', version='%(prog)s 0.1 Alpha')

# required argument for slack chat log folder location
parser.add_argument('location', action='store',
                    help='The path of the slack chat log folder')

# parse all the arguments in to the results variable to be referenced
results = parser.parse_args()


# set up the standard variables
rootdir = results.location # grab location from arguments that were parsed
ignored_files = ["channels.json", "integration_logs.json", "users.json"] # ignore files that don't need reading
messages = [] # create array which will store all messages for json file


File.writelogfile()
