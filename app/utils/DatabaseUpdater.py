from app.utils.WebUtils import WebUtils
from app.models import Olympiad, Event


class DatabaseUpdater():

    def __init__(self):
        self.webutils = WebUtils()

    def update_database(self):
        olympiads_info_list = self._get_olympiads_info_list()
        self._save_olympiads_info(olympiads_info_list)

    def _get_olympiads_info_list(self):
        # данный список будет браться с помощью других функци
        # сейчас он заполнен вручную ради проверки корректности
        olympiads_url_lists = ['https://olimpiada.ru/activity/5277',
                               'https://olimpiada.ru/activity/180',
                               'https://olimpiada.ru/activity/5149',
                               'https://olimpiada.ru/activity/5668',
                               'https://olimpiada.ru/activity/157',
                               'https://olimpiada.ru/activity/5319',
                               'https://olimpiada.ru/activity/232',
                               'https://olimpiada.ru/activity/177',
                               'https://olimpiada.ru/activity/5761',
                               'https://olimpiada.ru/activity/251']

        olympiads_info_list = list()
        for i, olympiad_url in enumerate(olympiads_url_lists):
            events_dict = \
                self.webutils.getEventsWithDeadlinesByUrl(olympiad_url)
            events_list = list()
            for name, date in events_dict.items():
                events_list.append({'event_name': name,
                                    'date_start': date,
                                    'date_end': None})
            olympiads_info_list.append({'olympiad_name': str(i),
                                        'olympiad_url': olympiad_url,
                                        'events': events_list})
            print(olympiads_info_list[-1])
        return olympiads_info_list

    def _save_olympiads_info(self, olympiads_info_list):
        for olympiad_info in olympiads_info_list:
            self._create_olympiad(name=olympiad_info['olympiad_name'],
                                  url=olympiad_info['olympiad_url'])
            for event in olympiad_info['events']:
                self._create_event(olympiad_id=Olympiad.get_id_by_url(
                    olympiad_info['olympiad_url']),
                    name=event['event_name'],
                    date_start=event['date_start'],
                    date_end=event['date_end'])

    @staticmethod
    def _create_olympiad(name, url=None):
        olympiad = Olympiad(name=name, url=url)
        olympiad.save()
        print(olympiad)

    @staticmethod
    def _create_event(olympiad_id, name, date_start=None, date_end=None):
        event = Event(olympiad_id=olympiad_id, name=name,
                      date_start=date_start, date_end=date_end)
        event.save()
        print(event)
