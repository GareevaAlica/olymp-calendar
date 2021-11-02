import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import pytz
from config import SERVICE_ACCOUNT_FILE

SCOPES = ['https://www.googleapis.com/auth/calendar']


def to_iso_extended(date):
    # date -= datetime.timedelta(days=180)
    return date.strftime("%Y-%m-%dT%H:%M:%S")


def from_iso_extended(str):
    return datetime.datetime.fromisoformat(str)


class GoogleCalendar():
    def __init__(self, calendar_id, credentials=None):
        if credentials is None:
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3',
                                                       credentials=credentials)
        self.calendar_id = calendar_id

    def create_event(self, event):
        e = self.service.events().insert(calendarId=self.calendar_id,
                                         body=event).execute()

        print('Event created: %s' % (e.get('id')))

    def olympiad_to_calendar_event(self, olympiad, olympiad_event):
        event = {
            'summary':
                f'{olympiad_event.event_name} :'
                f' {olympiad.olympiad_name[:50] + "..."}',
            'description':
                f'{olympiad_event.event_name} '
                f'<br>'
                f'<a href="{olympiad.olympiad_url}">{olympiad.olympiad_name}</a>',
            'start':
                {'dateTime': to_iso_extended(olympiad_event.date_start),
                 'timeZone': 'GMT+00:00'},
            'end':
                {'dateTime':
                    to_iso_extended(
                        olympiad_event.date_end if olympiad_event.date_end else olympiad_event.date_start),
                    'timeZone': 'GMT+00:00'},
        }
        return event

    def create_olympiad_events(self, olympiads: list, delete_all=True,
                               delete_outdated=False):
        if delete_all:
            self.delete_all_events()
        if delete_outdated:
            self.delete_legacy_events()
        for olympiad in olympiads:
            for olympiad_event in olympiad.events:
                self.create_event(
                    self.olympiad_to_calendar_event(olympiad, olympiad_event))


    def delete_selected_olympiads(self, olympiads):
        events_summaries_to_delete = []
        for olympiad in olympiads:
            if olympiad.olympiad_name in olympiads_names_to_delete:
                for event in olympiad.events:
                    events_summaries_to_delete.append(self.olympiad_to_calendar_event(olympiad, event)['summary'])
        page_token = None
        while True:
            events_result = self.service.events().list(calendarId=self.calendar_id,
                                                       singleEvents=True,
                                                       orderBy='startTime',
                                                       pageToken=page_token).execute()
            events = events_result.get('items', [])
            for event in events:
                if event['summary'] in events_summaries_to_delete:
                    self.service.events().delete(calendarId=self.calendar_id,
                                                 eventId=event['id']).execute()
            page_token = events_result.get('nextPageToken', [])
            if page_token == []:
                break


    def update_olympiad_events(self, old_olympiads, new_olympiads):
        set_old_olympiads = set(old_olympiads)
        set_new_olympiads = set(new_olympiads)
        olympiads_to_delete = set_old_olympiads - set_new_olympiads
        olympiads_to_create = set_new_olympiads - set_old_olympiads
        self.delete_selected_olympiads(olympiads_to_delete)
        self.create_olympiad_events(olympiads_to_create, delete_all=False, delete_outdated=True)


    def delete_legacy_events(self):
        datetime_now = datetime.datetime.utcnow()
        now = datetime_now.isoformat() + 'Z'
        finished = False
        while not finished:
            print('Deleting the upcoming 10 events')
            events_result = self.service.events().list(calendarId=self.calendar_id,
                                                       timeMax=now,
                                                       maxResults=10,
                                                       singleEvents=True,
                                                       orderBy='startTime').execute()
            events = events_result.get('items', [])
            if not len(events):
                break
            for event in events:
                if from_iso_extended(event['end']['dateTime']).replace(
                        tzinfo=pytz.UTC) < datetime_now.replace(
                    tzinfo=pytz.UTC):
                    self.service.events().delete(calendarId=self.calendar_id,
                                                 eventId=event['id']).execute()
                else:
                    finished = True

    def delete_all_events(self):
        pageToken = None
        while True:
            events_result = self.service.events().list(calendarId=self.calendar_id,
                                                       singleEvents=True,
                                                       orderBy='startTime',
                                                       pageToken=pageToken).execute()
            events = events_result.get('items', [])
            for event in events:
                self.service.events().delete(calendarId=self.calendar_id,
                                             eventId=event['id']).execute()
            pageToken = events_result.get('nextPageToken', [])
            if pageToken == []:
                break

    def create_calendar(self):
        calendar = {
            'summary': 'olymp-calendar',
            'timeZone': 'Europe/Moscow'
        }
        created_calendar = self.service.calendars().insert(
            body=calendar).execute()
        return created_calendar['id']
