from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from datetime import timedelta
import datetime
import pytz

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

service_account_email = 'abhijeet-pandey@quickstart-1599466419791.iam.gserviceaccount.com'

CLIENT_SECRET_FILE = 'PayApp/Calendar/creds.p12'

SCOPES = 'https://www.googleapis.com/auth/calendar'
scopes = [SCOPES]

def build_service():
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        service_account_email=service_account_email,
        filename=CLIENT_SECRET_FILE,
        scopes=SCOPES
    )

    http = credentials.authorize(httplib2.Http())

    service = build('calendar', 'v3', http=http)

    return service


def create_event():
    service = build_service()

    start_datetime = datetime.datetime.now(tz=pytz.utc)
    event = service.events().insert(calendarId='primary', body={
        'summary': 'Foo',
        'description': 'Bar',
        'start': {'dateTime': start_datetime.isoformat()},
        'end': {'dateTime': (start_datetime + timedelta(minutes=360)).isoformat()},
    }).execute()

    print(event)

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# def main():
#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'PayApp/Calendar/credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     service = build('calendar', 'v3', credentials=creds)

#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                         maxResults=10, singleEvents=True,
#                                         orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])


# if __name__ == '__main__':
#     main()

# # 670146120485-3rhhkg9t7mjhuldg0keg2t3souop7ek0.apps.googleusercontent.com
# # 58hmW1-jTXcHJM5Chp6dH-HR
#   #  # 654892145924-9lcm5tcbdneg3cks1ddd7790jhfc833o.apps.googleusercontent.com
#   #  # hA-NzgpMQ7QYGwpyAvx7OKqt

# #   // {"installed":{"client_id":"896659605185-dat9dopbkpq12llbiccee0255qbovrvb.apps.googleusercontent.com","project_id":"quickstart-1599462532027","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"nxJ82CW3JPjZNSlAub0G7vCG","redirect_uris":["urn:ietf:wg:oauth:2.0:oob","http://localhost"]}}