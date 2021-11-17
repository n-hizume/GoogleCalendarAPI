import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import json

# To Use Google API, Road a neccessary json file
def load_creds(account_name):

  creds = None
  SCOPES = ['https://www.googleapis.com/auth/calendar']

  account_folder = os.path.join('account', account_name)
  tokenfile = os.path.join(account_folder, 'token.picle')

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
          flow = InstalledAppFlow.from_client_secrets_file(os.path.join(account_folder, 'credentials.json'), SCOPES)
          creds = flow.run_local_server(port=0)

      with open(tokenfile, 'wb') as token:
          pickle.dump(creds, token)

  return build('calendar', 'v3', credentials=creds)

# load 'account/{account_name}/idlist.json and return its dict for python
def load_idlist(account_name):
    json_path = os.path.join('account', account_name, 'idlist.json')
    with open(json_path, 'rb') as file:
        return json.load(file)
