import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.models import Olympiad, Event


SCOPES = ['https://www.googleapis.com/auth/calendar']


calendarId = 'ju826grepi1c5aldl8jbill7as@group.calendar.google.com'
SERVICE_ACCOUNT_FILE = '../../keys/client_secret_529021305325-8vvgsbl0j5sh6r9gqdg3bvaflabc2cge.apps.googleusercontent.com.json'

class GoogleCalendar():
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)


    def create_event(self, event):
    	e = self.service.events().insert(calendarId=calendarId,
                                         body=event).execute()
        print('Event created: %s' % (e.get('id')))



	def olympiad_to_calendar_event(self, olympiad, olympiad_event):
		event = {
			'summary': f'{olympiad_event.get_name}:{olympiad.get_name}',
			'desciption': f'<a href="{olympiad.url}">{olympid.get_name}</a>',
			'start': olympiad_event.date_start
			'end': olympiad_event.date_end if olympiad_event.date_end else olympiad_event.date_start
		}
		return event


    def create_olympiad_events(self, olympiads : list, delete_outdated=True):
    	# if delete_outdated:
    	# 	self.delete_legacy_events()
    	for olympiad in olympiads:
    		for olympiad_event in olympiad.events:
    			self.create_event(olympiad_to_event(olympiad, olympiad_event))


    def get_events_list(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=calendarId,
                                                   timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])