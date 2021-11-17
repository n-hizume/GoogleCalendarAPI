from datetime import date, datetime

from .load import load_creds, load_idlist
from .event import Event, AllDayEvent
from .define_format import decord_date, decord_datetime


class CalendarManager:
    account_name = ''
    token = ''
    idlist = ''
    today = ''

    def __init__(self, account_name):
        self.account_name = account_name
        self.token = load_creds(account_name)
        self.idlist = load_idlist(account_name)
        self.today = date.today()

    # Get key list of "account/{account_name}/idlist.json"
    def get_key_list(self):
        return [ key for key in self.idlist.keys() ]

    # Get Calendar ID from idlist.json
    def get_id(self, key):
        return self.idlist[key]

    # Add a Schedule to your calendar by Model defined at "src/event.py"
    # And print Schedule info
    def write(self, id, event):
        body = event.get_json()
        post = self.token.events().insert(calendarId=id, body=body).execute()
        
        print(f'\n・Registration Success：{event.title}=========================')
        print(event.get_term())
        print()
        return post
    
    # Make AlldayEvent Model and Call write()
    def register_allday_event(self, id, st_date: date, fn_date:date, title='no title', location='', detail=''):
        event = AllDayEvent(
                    st_date=st_date,
                    fn_date=fn_date,
                    title=title,
                    location=location,
                    detail=detail
                )
        self.write(id, event)

    # Make Event Model and Call write()
    def register_event(self, id, st_dtime: datetime, fn_dtime: datetime, title='no title', location='', detail=''):
        event = Event(
            st_dtime=st_dtime,
            fn_dtime=fn_dtime,
            title=title,
            location=location,
            detail=detail
        )
        self.write(id, event)

    
            

    # Receive Scedule info And datetime's list
    # decord the list and register to schedule
    def add(self, id, year, month, datetimes_str='', title='no title', location='', detail='', rename=False):
        datetime_str_list = datetimes_str.split(',')
        for datetime_str in datetime_str_list:
            if datetime_str == '':
                continue

            st_datetime, fn_datetime = decord_datetime(year, month, datetime_str)

            new_title = title
            if rename:
                time_str = '(' + st_datetime.strftime('%H:%M') + '-' + fn_datetime.strftime('%H:%M') + ')'
                new_title += time_str

            self.register_event(id=id, st_dtime=st_datetime, fn_dtime=fn_datetime, title=new_title)
            
    # Receive Scedule info And date's list
    # decord the list and register to schedule
    def add_allday(self, id, year, month, dates_str='', title='no title', location='', detail=''):
        date_str_list = dates_str.split(',')
        for date_str in date_str_list:
            if date_str == '':
                continue
            
            st_date, fn_date = decord_date(year, month, date_str)

            self.register_allday_event(id=id, st_date=st_date, fn_date=fn_date, title=title, location=location, detail=detail)