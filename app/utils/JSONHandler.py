from datetime import datetime, date
from typing import NamedTuple
import json


class OlympiadInfoTuple(NamedTuple):
    olympiad_name: str
    olympiad_url: str
    events: list


class EventTuple(NamedTuple):
    event_name: str
    date_start: date
    date_end: date


class JSONHandler():
    @staticmethod
    def from_class_to_dict(olympiads_info_list):
        olympiads_info_json = list()
        for olympiads_info in olympiads_info_list:
            events_list = list()
            for event in olympiads_info.events:
                events_list.append({'event_name': event.event_name,
                                    'date_start': event.date_start,
                                    'date_end': event.date_end})
            olympiads_info_json.append(
                {'olympiad_name': olympiads_info.olympiad_name,
                 'olympiad_url': olympiads_info.olympiad_url,
                 'events': events_list})
        return olympiads_info_json

    @staticmethod
    def save_in_file(file_name, data):
        with open('test_db/' + file_name + '.json', 'w') as f:
            json.dump(data, f, default=str)

    @staticmethod
    def date_hook(json_dict):
        for (key, value) in json_dict.items():
            try:
                json_dict[key] = datetime.strptime(value, "%Y-%m-%d").date()
            except:
                pass
        return json_dict

    def get_from_file(self, file_name):
        f = open('test_db/' + file_name + '.json')
        return json.load(f, object_hook=self.date_hook)

    @staticmethod
    def from_dict_to_class(olympiads_info_json):
        olympiads_info_list = list()
        for olympiads_info in olympiads_info_json:
            events_list = list()
            for event in olympiads_info['events']:
                events_list.append(EventTuple(event['event_name'],
                                              event['date_start'],
                                              event['date_end']))
            olympiads_info_list.append(
                OlympiadInfoTuple(olympiads_info['olympiad_name'],
                                  olympiads_info['olympiad_url'],
                                  events_list))
        return olympiads_info_list
