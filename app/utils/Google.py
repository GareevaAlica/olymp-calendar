import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.models import Olympiad, Event
import json
import datetime
import pytz


SCOPES = ['https://www.googleapis.com/auth/calendar']

calendarId = 'ju826grepi1c5aldl8jbill7as@group.calendar.google.com'
SERVICE_ACCOUNT_FILE = 'keys/olymp-calendar-ab93d48d55ca.json'

def to_iso_extended(date):
    date-=datetime.timedelta(days=180)
    return date.strftime("%Y-%m-%dT%H:%M:%S")

def from_iso_extended(str):
    return datetime.datetime.fromisoformat(str)


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
            'summary': f'{olympiad_event.name}:{olympiad.name}',
            'description': f'<a href="{olympiad.url}">{olympiad.name}</a>',
            'start': {'dateTime' : to_iso_extended(olympiad_event.date_start), 'timeZone': 'GMT+00:00'},
            'end': {'dateTime' : to_iso_extended(olympiad_event.date_end if olympiad_event.date_end else olympiad_event.date_start), 'timeZone': 'GMT+00:00'},
        }
        return event


    def create_olympiad_events(self, olympiads: list, delete_outdated=True):
        if delete_outdated:
            self.delete_legacy_events()
        for olympiad in olympiads:
            for olympiad_event in olympiad.events:
                self.create_event(self.olympiad_to_calendar_event(olympiad, olympiad_event))


    def delete_legacy_events(self):
        datetime_now = datetime.datetime.utcnow()
        now = datetime_now.isoformat() + 'Z'
        finished = False
        while not finished:
            print('Deleting the upcoming 10 events')
            events_result = self.service.events().list(calendarId=calendarId,
                                                       timeMax=now,
                                                       maxResults=10, singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])
            if not len(events):
                break
            for event in events:
                if from_iso_extended(event['end']['dateTime']).replace(tzinfo=pytz.UTC) < datetime_now.replace(tzinfo=pytz.UTC):
                    self.service.events().delete(calendarId=calendarId, eventId=event['id']).execute()
                else:
                    finished = True