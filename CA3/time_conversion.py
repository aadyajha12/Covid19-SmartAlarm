from datetime import datetime


def minutes_to_seconds(minutes) -> int:
    """Converts minutes to seconds"""
    return int(minutes) * 60


def hours_to_minutes(hours) -> int:
    """Converts hours to minutes"""
    return int(hours) * 60


def hhmm_to_seconds(hhmm: str):
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])


def hhmmss_to_seconds(hhmmss: str):
    if len(hhmmss.split(':')) != 3:
        print('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    else:
        return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
               minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])


def time_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time