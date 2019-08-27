from uuid import uuid5, NAMESPACE_URL
import datetime


def get_datetime_now_in_msec():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


def generate_random_str():
    now = get_datetime_now_in_msec()
    random = str(uuid5(NAMESPACE_URL, str(now)))
    return random.split("-")[0]
