import re
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


# re expression
re_day = '([0-9]{1,2})'
re_days = '([0-9]{1,2})'
re_time = '([0-9]{1,2}|[0-9]{1,2}:[0-9]{1,2})'


# Receive re_time<string>, such as '06:30', '7:00', '9', and Return (hour, minute)<int>
def decode_re_time(strtime):
    m = re.fullmatch('([0-9]{1,2}):([0-9]{1,2})', strtime)
    if m:
        [hour, minute] = [int(v) for v in m.groups()]
    else:
        hour = int(strtime)
        minute = 0

    if 24 <= hour:
        return hour-24, minute, True
    else:
        return hour, minute, False

# 1. '{day}*{days}'
# 2. '{day}-{day}': if day.second < day.first, day.second is judged as next month
# 3. '{day}'
# return st_date, fn_date
def decode_date(year, month, date_str):
    pattern1 = f'{re_day}\*{re_days}'
    pattern2 = f'{re_day}-{re_day}'
    pattern3 = f'{re_day}'

    m = re.fullmatch(pattern1, date_str)
    if m:
        [day, days] = [int(v) for v in m.groups()]
        st_date = date(year, month, day)
        fn_date = st_date + timedelta(days=days-1)
        return st_date, fn_date

    m = re.fullmatch(pattern2, date_str)
    if m:
        [st_day, fn_day] = [int(v) for v in m.groups()]
        st_date = date(year, month, st_day)
        fn_date = date(year, month, fn_day)
        if st_date < fn_date:
            return st_date, fn_date

        fn_date += relativedelta(months=1)
        return st_date, fn_date

    m = re.fullmatch(pattern3, date_str)
    if m:
        day = int(m.group())
        st_date = date(year, month, day)
        return st_date, st_date


# if time >= '24:00', time will be judged as tommorow
# 1. '{day}/{time}+{time}
# 2. '{day}/{time}-{time}: if time.first > time.second, time.second will be judged as tommorow
# 3. '{day}/{time}
# return st_datetime, fn_datetime
def decode_datetime(year, month, datetime_str):
    pattern1 = f'{re_day}/{re_time}\+{re_time}'
    pattern2 = f'{re_day}/{re_time}-{re_time}'
    pattern3 = f'{re_day}/{re_time}'

    m = re.fullmatch(pattern1, datetime_str)
    if m:
        [day, st_time, delta_time] = m.groups()
        day = int(day)

        st_h, st_m, inc = decode_re_time(st_time)
        st_datetime = datetime(year, month, day, st_h, st_m)
        if inc:
            st_datetime += timedelta(days=1)

        delta_h, delta_m, inc = decode_re_time(delta_time)
        if inc:
            delta_h += 24
        fn_datetime = st_datetime + timedelta(hours=delta_h, minutes=delta_m)

        return st_datetime, fn_datetime

    m = re.fullmatch(pattern2, datetime_str)
    if m:
        [day, st_time, fn_time] = m.groups()
        day = int(day)

        st_h, st_m, st_inc = decode_re_time(st_time)
        st_datetime = datetime(year, month, day, st_h, st_m)
        if st_inc:
            st_datetime += timedelta(days=1)

        fn_h, fn_m, fn_inc = decode_re_time(fn_time)
        fn_datetime = datetime(year, month, day, fn_h, fn_m)
        if fn_inc or st_datetime > fn_datetime:
            fn_datetime += timedelta(days=1)

        return st_datetime, fn_datetime

    m = re.fullmatch(pattern3, datetime_str)
    if m:
        [day, st_time] = m.groups()
        day = int(day)
        st_h, st_m, inc = decode_re_time(st_time)
        st_datetime = datetime(year, month, day, st_h, st_m)
        if inc:
            st_datetime += timedelta(days=1)

        return st_datetime, st_datetime
