import googleapiclient
from googleapiclient.discovery import build
import datetime


def to_iso_extended(date):
    # date -= datetime.timedelta(days=180)
    return date.strftime("%Y-%m-%dT%H:%M:%S")


def from_iso_extended(str):
    return datetime.datetime.fromisoformat(str)


class GoogleCalendar():
    def __init__(self, calendar_id, credentials=None):
        self.service = googleapiclient.discovery.build('calendar', 'v3',
                                                       credentials=credentials)
        self.calendar_id = calendar_id

    def create_event(self, event):
        e = self.service.events().insert(calendarId=self.calendar_id,
                                         body=event).execute()

        print('Event created: %s' % (e.get('summary')))

    def olympiad_to_calendar_event(self, olympiad, olympiad_event):
        event = {
            'summary':
                f'{olympiad_event.name} :'
                f' {olympiad.name[:50] + "..."}',
            'description':
                f'{olympiad_event.name} '
                f'<br>'
                f'<a href="{olympiad.url}">{olympiad.name}</a>',
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

    def create_olympiad_events(self, olympiads, delete_all=True):
        if delete_all:
            self.delete_all_events()
        for olympiad in olympiads:
            for olympiad_event in olympiad.events:
                self.create_event(
                    self.olympiad_to_calendar_event(olympiad, olympiad_event))

    def delete_selected_olympiads(self, olympiads):
        olympiads_names_to_delete = set()
        for olympiad in olympiads:
            olympiads_names_to_delete.add(olympiad.name)
        page_token = None
        while True:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                singleEvents=True,
                orderBy='startTime',
                pageToken=page_token).execute()
            events = events_result.get('items', [])
            for event in events:
                olympiads_name = event['description'].split("\">")[1][:-4]
                if olympiads_name in olympiads_names_to_delete:
                    self.service.events().delete(calendarId=self.calendar_id,
                                                 eventId=event['id']).execute()
                    print('Event deleted: %s' % (event['summary']))
            page_token = events_result.get('nextPageToken', [])
            if page_token == []:
                break

    def update_olympiad_events(self, all_olympiads_list,
                               old_olympiads_ids, new_olympiads_ids):
        set_old_olympiads_ids = set(old_olympiads_ids)
        set_new_olympiads_ids = set(new_olympiads_ids)
        olympiads_to_delete_ids = set_old_olympiads_ids - set_new_olympiads_ids
        olympiads_to_create_ids = set_new_olympiads_ids - set_old_olympiads_ids
        print('Delete:', olympiads_to_delete_ids)
        print('Create:', olympiads_to_create_ids)

        olympiads_to_delete = \
            self.get_olympiads_class_list(all_olympiads_list,
                                         olympiads_to_delete_ids)
        olympiads_to_create = \
            self.get_olympiads_class_list(all_olympiads_list,
                                         olympiads_to_create_ids)
        self.delete_selected_olympiads(olympiads_to_delete)
        self.create_olympiad_events(olympiads_to_create, delete_all=False)

    def delete_all_events(self):
        pageToken = None
        while True:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
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

    @staticmethod
    def get_olympiads_class_list(olympiads_list, indexes=None):
        if indexes is None:
            indexes = set(range(1, len(olympiads_list) + 1))
        else:
            indexes = set(map(int, indexes))
        olympiads_class_list = list()
        for olympiad in olympiads_list:
            if olympiad.id in indexes:
                olympiads_class_list.append(olympiad)
        return olympiads_class_list
