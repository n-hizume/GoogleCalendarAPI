from datetime import date, datetime, timedelta

# Give these Model to CalendarManagar, and Register Google Calendar

# get_json(): Convert Model to json for Google API
# get_term(): get <str> '{start_datetime}~{finish_datetime}'

class Event:
    def __init__(self, st_dtime: datetime, fn_dtime: datetime, title, location, detail):
        self.st_dtime = st_dtime
        self.fn_dtime = fn_dtime
        self.title = title
        self.location = location
        self.detail = detail

    def get_json(self):
        return {
            'summary': self.title,
            'location': self.location,
            'description': self.detail,
            'start': {
                'dateTime': self.st_dtime.isoformat(),
                'timeZone': 'Japan',
            },
            'end': {
                'dateTime': self.fn_dtime.isoformat(),
                'timeZone': 'Japan',
            }
        }

    def get_term(self):
      return self.st_dtime.strftime('%Y/%m/%d %H:%M') +' ~ '+ self.fn_dtime.strftime('%Y/%m/%d %H:%M')


class AllDayEvent:
    def __init__(self, st_date: date, fn_date: date, title, location, detail):
        self.st_date = st_date
        self.fn_date = fn_date
        self.title = title
        self.location = location
        self.detail = detail

    def get_json(self):
      return {
          'summary': self.title,
          'location': self.location,
          "allDayEvent": True,
          'description': self.detail,
          'start': {
              'date': self.st_date.strftime('%Y-%m-%d'),
              'timeZone': 'Japan',
          },
          'end': {
              'date': (self.fn_date + timedelta(days=1)).strftime('%Y-%m-%d'),
              'timeZone': 'Japan',
          }
      }
    
    def get_term(self):
      if self.st_date == self.fn_date:
        return self.st_date.strftime('%Y/%m/%d')
      else:
        return self.st_date.strftime('%Y/%m/%d') +' ~ '+ self.fn_date.strftime('%Y/%m/%d')