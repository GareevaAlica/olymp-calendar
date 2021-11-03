from datetime import date
from typing import NamedTuple


class OlympiadInfoTuple(NamedTuple):
    olympiad_name: str
    olympiad_url: str
    events: list
    classes: str
    fields: list


class EventTuple(NamedTuple):
    event_name: str
    date_start: date
    date_end: date


def get_olympiads_info_list(olympiads_list, indexes=None):
    if indexes is None:
        indexes = [i for i in range(1, len(olympiads_list) + 1)]
    olympiads_info_list = list()
    for index in indexes:
        olympiad = olympiads_list[int(index) - 1]
        events_list = list()
        for event in olympiad.events:
            events_list.append(EventTuple(event.name,
                                          event.date_start,
                                          event.date_end))
        olympiads_info_list.append(
            OlympiadInfoTuple(olympiad.name,
                              olympiad.url,
                              events_list,
                              olympiad.classes,
                              olympiad.fields))
    return olympiads_info_list
