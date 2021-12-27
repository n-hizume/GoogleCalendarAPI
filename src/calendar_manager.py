import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os.path
import json
from datetime import date



class CalendarManager:
    account_name = ''
    account_folder = ''
    service = ''
    idlist = ''
    today = ''

    def __init__(self, account_name):
        self.account_name = account_name
        self.account_folder = os.path.join('account', self.account_name)
        self.service = self.load_creds()
        self.idlist = self.load_idlist()
        self.today = date.today()

    # To Use Google API, Road a neccessary json file
    def load_creds(self):
        creds = None
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        tokenfile = os.path.join(self.account_folder, 'token.picle')

        # if you have token file
        if os.path.exists(tokenfile):
            with open(tokenfile, 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            # if token file is not available
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            # if you don't have token file
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(self.account_folder, 'credentials.json'), SCOPES)
                creds = flow.run_local_server(port=0)

            with open(tokenfile, 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)
    
    # load 'account/{account_name}/idlist.json and return its dict for python
    def load_idlist(self):
        json_path = os.path.join( self.account_folder, 'idlist.json')
        with open(json_path, 'rb') as file:
            return json.load(file)

    # Get key list of "account/{account_name}/idlist.json"
    def get_key_list(self):
        return [ key for key in self.idlist.keys() ]

    # Get Calendar ID from idlist.json
    def get_id(self, key):
        return self.idlist[key]

    # Add a Schedule to your calendar by Model defined at "src/event.py"
    # And print Schedule info
    def write(self, id, event):
        body = event.get_body()
        post = self.service.events().insert(calendarId=id, body=body).execute()
        
        return post