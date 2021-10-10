from app.utils.WebUtils import WebUtils
from app.models import Olympiad, Event
from datetime import date
import re


# Класс заполнения базы данных информацией об олимпиадах
class DatabaseUpdater():
    # данный список будет браться с помощью других функций
    # сейчас он заполнен вручную ради проверки корректности
    all_olympiads_url_list = ['https://olimpiada.ru/activity/5023',
                              'https://olimpiada.ru/activity/182',
                              'https://olimpiada.ru/activity/5277',
                              'https://olimpiada.ru/activity/251']

    def __init__(self):
        # класс обработки web страниц
        self.webutils = WebUtils()

    def update_database(self):
        """
        Обновление базы данных информацией об олимпиадах
        :return: None
        """
        # получаем кончательные ссылки на олимпиады
        olympiads_url_dict = \
            self.__get_olympiads_url_dict(self.all_olympiads_url_list)
        # получаем информацию об олимпиадах
        olympiads_info_list = \
            self.__get_olympiads_info_list(olympiads_url_dict)
        # сохраняем олимпиады и их события в базу данных
        self.__save_olympiads_info(olympiads_info_list)

    def __get_olympiads_url_dict(self, all_olympiads_url_list):
        olympiads_url_dict = dict()
        for i, all_olympiads_url in enumerate(all_olympiads_url_list):
            try:
                related_olympiads = \
                    self.webutils.getRelatedOlympiadsByUrl(all_olympiads_url)
            except RuntimeError:
                olympiads_url_dict['Olympiad' + str(i)] = all_olympiads_url
            else:
                for olympiad_name, olympiads_url in related_olympiads.items():
                    olympiads_url_dict[olympiad_name] = \
                        'https://olimpiada.ru' + olympiads_url
        print(olympiads_url_dict)
        return olympiads_url_dict

    def __get_olympiads_info_list(self, olympiads_url_dict):
        """
        Получение информации об олимпиадах
        :param olympiads_url_lists: ссылки на олимпиады
        :return: list({'olympiad_name': string,
                    'olympiad_url': string,
                    'events': list({'event_name': string,
                                    'date_start': string,
                                    'date_end': string
                                    }, ...),
                    }, ...)
        """

        olympiads_info_list = list()
        for olympiad_name, olympiad_url in olympiads_url_dict.items():
            # получение информацию о расписании событий олимпиады по url
            events_dict = \
                self.webutils.getEventsWithDeadlinesByUrl(olympiad_url)
            events_list = list()
            # обработка событий в расписании олимпиады
            for event_name, date in events_dict.items():
                date_start_end = self.__get_date_start_end(date)
                events_list.append({'event_name': event_name,
                                    'date_start': date_start_end['date_start'],
                                    'date_end': date_start_end['date_end']})
            olympiads_info_list.append({'olympiad_name': olympiad_name,
                                        'olympiad_url': olympiad_url,
                                        'events': events_list})
            print(olympiads_info_list[-1])
        return olympiads_info_list

    def __save_olympiads_info(self, olympiads_info_list):
        """
        Сохранение олимпиад и их событий в базу данных
        :param olympiads_info_list: информация об олимпиадах
        list({'olympiad_name': string,
            'olympiad_url': string,
            'events': list({'event_name': string,
                            'date_start': string,
                            'date_end': string
                            }, ...),
            }, ...)
        :return: None
        """
        for olympiad_info in olympiads_info_list:
            olympiad_id = \
                self.__create_olympiad(name=olympiad_info['olympiad_name'],
                                       url=olympiad_info['olympiad_url'])
            for event in olympiad_info['events']:
                self.__create_event(olympiad_id=olympiad_id,
                                    name=event['event_name'],
                                    date_start=event['date_start'],
                                    date_end=event['date_end'])

    @staticmethod
    def __create_olympiad(name, url=None):
        """
        Сохранение олимпиады в базу данных
        :param name: название олимпиады
        :param url: url олимпиады
        :return: id сохраненной олимпиады
        """
        olympiad = Olympiad(name=name, url=url)
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
