import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def check_calendar_events():

  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  
  if os.path.exists("utilities/token.json"):
    creds = Credentials.from_authorized_user_file("utilities/token.json", SCOPES)
  if not creds or not creds.valid:
    logging.info("No valid credentials.")
    
    if creds and creds.expired and creds.refresh_token:      
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file("utilities/credentials.json", SCOPES)      
      creds = flow.run_local_server() 
      
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    logging.info("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    logging.info(events)
    
    if not events:
      logging.info("No upcoming events found.")
      return

    events_list = []
    for event in events:
      start = event["start"].get("dateTime")
      start_object = datetime.datetime.fromisoformat(start)
      formatted_start =start_object.strftime('%A %B %d of %Y at %I:%M %p')

      end = event["end"].get("dateTime")
      end_object = datetime.datetime.fromisoformat(end)
      formatted_end =end_object.strftime('%A %B %d of %Y at %I:%M %p')
       
      summary = event["summary"]

      event = {
        "start": formatted_start,
        "end": formatted_end,
        "summary": summary
      }
      events_list.append(event)      
    logging.info("List of events: ",events_list)
    return events_list

  except Exception as e:
        logging.exception("Unexpected error occurred when checking calendar events.")
        return ({"detail": " An unexpected error occurred, " + str(e)})