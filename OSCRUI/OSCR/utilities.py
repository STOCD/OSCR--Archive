from datetime import datetime

from .datamodels import LogLine

def to_datetime(date_time:str) -> datetime:
    '''
    returns datetime object from combatlog string containing date and time
    '''
    date_time_list = date_time.split(':')
    date_time_list += date_time_list.pop().split('.')
    date_time_list = list(map(int, date_time_list))
    date_time_list[0] += 2000
    date_time_list[6] *= 100000
    return datetime(*date_time_list)

def datetime_to_str(date_time:datetime) -> str:
    '''
    Converts datetime object to str timestamp. Truncates microseconds to tenth of seconds.
    '''
    return (f'{str(date_time.year)[-2:]}:{date_time.month:02d}:{date_time.day:02d}:{date_time.hour:02d}:'
            f'{date_time.minute:02d}:{date_time.second:02d}.{str(date_time.microsecond)[0]}')

def datetime_to_display(date_time:datetime) -> str:
    '''
    Converts datetime object to formatted string.
    '''
    return (f'{date_time.year}-{date_time.month:02d}-{date_time.day:02d} {date_time.hour:02d}:'
            f'{date_time.minute:02d}:{date_time.second:02d}')

def logline_to_str(line:LogLine | str) -> str:
    '''
    Converts LogLine to str or returns str if argument is str.
    '''
    if isinstance(line, str):
        return line.strip() + '\n'
    
    timestamp = datetime_to_str(line.timestamp)
    return f'{timestamp}::{','.join(line[1:11])},{line[11]},{line[12]}\n'