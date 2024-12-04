import datetime

def _check_suitable_datetime(datetime_to_check):
    # diff = _get_time() - datetime_to_check
    print(_get_time(), datetime_to_check)
    print(_get_time().hour, datetime_to_check.hour)
    # and 
    return _get_time().day <= datetime_to_check.day and datetime_to_check.hour > 8 and datetime_to_check.hour < 17

def _get_time():
    return datetime.datetime.now(datetime.timezone.utc)