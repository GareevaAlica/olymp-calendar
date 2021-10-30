from app.utils.WebUtils import WebUtils
from app.utils.JSONHandler import JSONHandler
from app.models import Olympiad, Event
from datetime import date
from typing import NamedTuple
import re


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


# Класс заполнения базы данных информацией об олимпиадах
class DatabaseUpdater():
    olympiad_map_url = 'https://olimpiada.ru/article/973'

    def __init__(self):
        self.json_handler = JSONHandler()

    def save_olympiads_info_from_json(self):
        olympiads_info_list = \
            self.json_handler.from_dict_to_class(
                self.json_handler.get_from_file('olympiads_info_list'))
        self.__save_olympiads_info(olympiads_info_list)

    def update_database(self, save_test_db=False):
        """
        Обновление базы данных информацией об олимпиадах
        :return: None
        """
        # получаем ссылки на страницы олимпиад.
        # среди них могут быть страницы,
        # которые содержат в себе еще один список олимпиад
        # и "окончательные" ссылки, которые имеют раписание
        all_olympiads_url_dict = \
            WebUtils.getMapNameLink(self.olympiad_map_url)
        if save_test_db:
            self.json_handler.save_in_file('olympiads_map',
                                           all_olympiads_url_dict)
        print('Got Olympiads Map:', len(all_olympiads_url_dict))

        # получаем "окончательные" ссылки на олимпиады
        olympiads_url_dict = \
            self.__get_olympiads_url_dict(all_olympiads_url_dict)
        if save_test_db:
            self.json_handler.save_in_file('olympiads_url', olympiads_url_dict)
        print('Got Olympiads url dict', len(olympiads_url_dict))

        # получаем информацию об олимпиадах
        olympiads_info_list = \
            self.__get_olympiads_info_list(olympiads_url_dict)
        if save_test_db:
            self.json_handler.save_in_file('olympiads_info_list',
                                           self.json_handler.from_class_to_dict(
                                               olympiads_info_list))
        print('Got Olympiads Info List', len(olympiads_info_list))

        # сохраняем олимпиады и их события в базу данных
        self.__save_olympiads_info(olympiads_info_list)
        print('DONE!')

    def __get_olympiads_url_dict(self, all_olympiads_url_dict):
        olympiads_url_dict = dict()
        for i, (all_olympiad_name, all_olympiad_url) in \
                enumerate(all_olympiads_url_dict.items()):
            if all_olympiad_url is None:
                olympiads_url_dict[all_olympiad_name] = None
                continue
            try:
                related_olympiads = \
                    WebUtils.getRelatedOlympiadsByUrl(all_olympiad_url)
            except RuntimeError:
                olympiads_url_dict[all_olympiad_name] = all_olympiad_url
            else:
                for olympiad_name, olympiad_url in related_olympiads.items():
                    olympiads_url_dict[olympiad_name] = \
                        'https://olimpiada.ru' + olympiad_url
            print('[{} | {}] {}'.format(i + 1, len(all_olympiads_url_dict),
                                        all_olympiad_name))
        return olympiads_url_dict

    def __get_olympiads_info_list(self, olympiads_url_dict):
        """
        Получение информации об олимпиадах
        :param olympiads_url_lists: ссылки на олимпиады
        :return: list(OlympiadInfoTuple)
        """

        olympiads_info_list = list()
        for i, (olympiad_name, olympiad_url) \
                in enumerate(olympiads_url_dict.items()):
            if olympiad_url is None:
                continue
            # получение информацию об олимпиаде по url
            olympiad_info = WebUtils.getOlympiadInfoByUrl(olympiad_url)
            # информация о расписании событий
            events_dict = olympiad_info.eventToDeadline
            events_list = list()
            # обработка событий в расписании олимпиады
            for event_name, date in events_dict.items():
                date_start_end = self.__get_date_start_end(date)
                events_list.append(EventTuple(event_name,
                                              date_start_end['date_start'],
                                              date_start_end['date_end']))
            olympiads_info_list.append(OlympiadInfoTuple(olympiad_name,
                                                         olympiad_url,
                                                         events_list,
                                                         olympiad_info.classes,
                                                         olympiad_info.fields))
            print('[{} | {}] {}'.format(i + 1, len(olympiads_url_dict),
                                        olympiads_info_list[-1].olympiad_name))
        return olympiads_info_list

    def __save_olympiads_info(self, olympiads_info_list):
        """
        Сохранение олимпиад и их событий в базу данных
        :param olympiads_info_list: информация об олимпиадах
        list(OlympiadInfoTuple)
        :return: None
        """
        for olympiad_info in olympiads_info_list:
            olympiad_id = \
                self.__create_olympiad(name=olympiad_info.olympiad_name,
                                       url=olympiad_info.olympiad_url,
                                       classes=olympiad_info.classes)
            for event in olympiad_info.events:
                self.__create_event(olympiad_id=olympiad_id,
                                    name=event.event_name,
                                    date_start=event.date_start,
                                    date_end=event.date_end)
            Olympiad.save_field_list(olympiad_id, olympiad_info.fields)

    @staticmethod
    def __create_olympiad(name, url=None, classes=None):
        """
        Сохранение олимпиады в базу данных
        :param name: название олимпиады
        :param url: url олимпиады
        :return: id сохраненной олимпиады
        """
        olympiad = Olympiad(name=name, url=url, classes=classes)
        id = olympiad.save()
        print(olympiad)
        return id

    @staticmethod
    def __create_event(olympiad_id, name, date_start=None, date_end=None):
        """
        Сохранение события в базу данных
        :param olympiad_id: id оимпиады в базе данных,
                            которой пренадлежит событие
        :param name: название события
        :param date_start: дата начала проведения события
        :param date_end: дата конца проведения события
        :return: id сохраненного события
        """
        event = Event(olympiad_id=olympiad_id, name=name,
                      date_start=date_start, date_end=date_end)
        id = event.save()
        print(event)
        return id

    def __get_date_start_end(self, date):
        dates = re.sub('[...]', ' ', date).split()
        date_start = None
        date_end = None
        if dates[0] == 'До':
            date_start = self.__transform_date(int(dates[1]), dates[2])
        elif len(dates) == 4:
            date_start = self.__transform_date(int(dates[0]), dates[1])
            date_end = self.__transform_date(int(dates[2]), dates[3])
        elif len(dates) == 3:
            date_start = self.__transform_date(int(dates[0]), dates[2])
            date_end = self.__transform_date(int(dates[1]), dates[2])
        else:
            date_start = self.__transform_date(int(dates[0]), dates[1])
        return {'date_start': date_start,
                'date_end': date_end}

    @staticmethod
    def __transform_date(day, month):
        months_dict = dict(zip(['янв', 'фев', 'мар',
                                'апр', 'май', 'июн',
                                'июл', 'авг', 'сен',
                                'окт', 'ноя', 'дек'], range(1, 13)))
        month_number = months_dict[month]
        year = 2021
        if month_number < 9:
            year = 2022
        return date(year, month_number, day)
