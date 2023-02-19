from datetime import date, datetime, timedelta

# Give these Model to CalendarManagar, and Register Google Calendar

# get_body(): Convert Model to json for Google API
# get_term(): get <str> '{start_datetime}~{finish_datetime}'

class Event:

    def __init__(self, title='no title', location='', detail=''):
        self.title = title
        self.location = location
        self.detail = detail
        self.timezone = 'Japan'

    def get_body(self):
        return {
            'summary': self.title,
            'description': self.detail,
            'location': self.location,
            'start': { 'timeZone': self.timezone },
            'end': { 'timeZone': self.timezone }
        }
    
        
class NormalEvent(Event):
    def __init__(self, st_dtime: datetime, fn_dtime: datetime, title='no title', location='', detail=''):
        super().__init__(title, location, detail)
        self.st_dtime = st_dtime
        self.fn_dtime = fn_dtime

    def get_body(self):
        body = super().get_body()
        body['start']['dateTime'] = self.st_dtime.isoformat(),
        body['end']['dateTime'] = self.fn_dtime.isoformat(),

        
        return body

    def get_term(self):
      return self.st_dtime.strftime('%Y/%m/%d %H:%M') +' ~ '+ self.fn_dtime.strftime('%Y/%m/%d %H:%M')


class AllDayEvent(Event):
    def __init__(self, st_date: date, fn_date: date, title='no title', location='', detail=''):
        super().__init__(title, location, detail)
        self.st_date = st_date
        self.fn_date = fn_date

    def get_body(self):
        body = super().get_body()
        body['allDayEvent'] = True
        body['start']['date'] = self.st_date.strftime('%Y-%m-%d')
        body['end']['date'] = (self.fn_date + timedelta(days=1)).strftime('%Y-%m-%d')

        return body

    def get_term(self):
      if self.st_date == self.fn_date:
        return self.st_date.strftime('%Y/%m/%d')
      else:
        return self.st_date.strftime('%Y/%m/%d') +' ~ '+ self.fn_date.strftime('%Y/%m/%d')