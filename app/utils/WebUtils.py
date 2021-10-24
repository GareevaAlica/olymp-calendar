import requests
from bs4 import BeautifulSoup
import re


class WebUtils:
    @staticmethod
    def getHtmlByUrl(url):
        response = requests.get(url)
        return response.content

    @staticmethod
    def getOlympiadInfoByUrl(url):
        html = WebUtils.getHtmlByUrl(url)
        soup = BeautifulSoup(html, 'html.parser')

        return OlympiadInfo(
            WebUtils.getEventToDeadline(soup),
            WebUtils.getClasses(soup),
            WebUtils.getFields(soup))

    @staticmethod
    def getEventToDeadline(soup):
        event_tokens = WebUtils.__getEventTokens(soup)
        if not event_tokens:
            return {}
        if len(event_tokens) % 2:
            event_tokens.pop()

        events = [event_tokens[i].contents[0].contents[0]
                  for i in range(0, len(event_tokens), 2)]
        event_deadlines = [event_tokens[i].contents[0]
                           for i in range(1, len(event_tokens), 2)]

        eventToDeadline = dict()

        for i in range(0, len(events)):
            eventToDeadline[events[i]] = event_deadlines[i].replace('\xa0', ' ')

        return eventToDeadline

    @staticmethod
    def __getEventTokens(soup):
        events = soup.findAll(
            'a',
            attrs={'href': re.compile(r"/activity/.*/events/*")}
        )
        return events

    @staticmethod
    def getClasses(soup):
        classesTokens = WebUtils.__getClassesTokens(soup)
        if not classesTokens:
            return ""
        classes = classesTokens[0].text
        return classes[:classes.find(' ')]

    @staticmethod
    def __getClassesTokens(soup):
        classesTokens = soup.findAll(
            'span',
            attrs={'class': 'classes_types_a'}
        )
        return classesTokens

    @staticmethod
    def getFields(soup):
        fieldsTokens = WebUtils.__getFieldsTokens(soup)
        if not fieldsTokens:
            return list()

        return list(map(lambda token: token.text.replace('\xa0', ' ').strip(), fieldsTokens))

    @staticmethod
    def __getFieldsTokens(soup):
        fieldsTokens = soup.findAll(
            'span',
            attrs={'class': 'subject_tag small-tag'}
        )
        return fieldsTokens

    @staticmethod
    def getMapNameLink(url: str) -> dict:
        res = dict()
        soup = list(BeautifulSoup(
            WebUtils.getHtmlByUrl(url),
            'html.parser'
        ).find_all('li'))[:-1]
        for elem in soup:
            if not isinstance(elem.contents[0], str):
                res[elem.contents[0].contents[0]] = elem.contents[0]['href']
            elif len(elem.contents) > 4:
                res[elem.contents[0] + elem.contents[1].contents[0]] = \
                    elem.contents[1]['href']
                res[elem.contents[0] + elem.contents[3].contents[0]] = \
                    elem.contents[3]['href']
            else:
                res[elem.contents[0]] = None
        return res

    @staticmethod
    def getRelatedOlympiadsByUrl(url):
        htmlDoc = WebUtils.getHtmlByUrl(url)

        olympiad_tokens = WebUtils.__getOlympiadsTokensFromHtml(htmlDoc)
        olympiad_tokens = olympiad_tokens[1::2]

        try:
            olympiads = [
                (olympiad_token.contents[1].contents[0], olympiad_token['href'])
                for olympiad_token in olympiad_tokens]
        except AttributeError as err:
            # print(f'Attribure Error: {err}')
            raise RuntimeError('Unknown format of webpage')
        except IndexError as err:
            # print(f'Index Error: {err}')
            raise RuntimeError('Unknown format of webpage')

        nameToLink = dict(olympiads)

        return nameToLink

    @staticmethod
    def __getOlympiadsTokensFromHtml(html):
        soup = BeautifulSoup(html, 'html.parser')
        olympiads = soup.findAll('a',
                                 attrs={'href': re.compile(r"/activity/\d*$")})
        return olympiads


class OlympiadInfo:
    eventToDeadline: dict
    classes: str
    fields: list

    def __init__(self, eventToDeadline, classes, fields):
        self.eventToDeadline = eventToDeadline
        self.classes = classes
        self.fields = fields
