import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager


# driver = webdriver.Chrome(ChromeDriverManager().install())
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
chrome = os.path.join(os.getcwd(), "chromedriver")
def check_calendar_events():
# def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    print("No valid creds ============")
    if creds and creds.expired and creds.refresh_token:
      print("Exp creds+++++++++++++++")
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "utilities/credentials.json", SCOPES
      )
      print("creds before::::::::::::::::::",creds)
      
      creds = flow.run_local_server(bind_addr="0.0.0.0",open_browser=False,port=10000,browser='chrome')
                                    
      
      print("creds::::::::::::::::::",creds)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
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
    print(events)
    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      end = event["end"].get("dateTime", event["end"].get("date"))
      print(start, event["summary"])
      #print(end, type(end))
    return start, end, event["summary"]

  except Exception as e:
        print(e)


# if __name__ == "__main__":
#   main()
        

