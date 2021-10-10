from app import db
import requests
from bs4 import BeautifulSoup
import re
from array import array

# Файл для классов базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

class WebUtils():
    @staticmethod
    def getHtmlByUrl(url):
        response = requests.get(url)
        return response.content

    @staticmethod
    def getEventsWithDeadlinesByUrl(url):
        eventToDeadline = dict()

        htmlDoc = WebUtils.getHtmlByUrl(url)

        event_tokens = WebUtils.__getEventsFromHtml(htmlDoc)
        events_tokens.pop()

        events = [event_tokens[i].contents[0].contents[0] for i in range(0, len(event_tokens), 2)]
        event_deadlines = [event_tokens[i].contents[0] for i in range(1, len(event_tokens), 2)]

        for i in range(0, len(events)):
            eventToDeadline[events[i]] = event_deadlines[i]

        return eventToDeadline

    @staticmethod
    def __getEventTokensFromHtml(html):
        soup = BeautifulSoup(html, 'html.parser')
        events = soup.findAll('a', attrs={'href': re.compile(r"/activity/.*/events/*")})
        return events
