import datetime
import hashlib
from pathlib import Path

import pytz


localtz = datetime.datetime.now().astimezone().tzinfo


def get_filehash(path):
    with open(path, "rb") as f:
        hasher = hashlib.md5()
        hasher.update(f.read())
        filehash = hasher.hexdigest()
    return filehash if filehash else None


def utc_datetime_to_local(dt):
    return dt.replace(tzinfo=pytz.timezone("utc")).astimezone(localtz)


def validate_file_path(filepath):
    if not Path(filepath).is_file():
        raise PathIsNotValidError


def header_string(strn, pattern="#", length=80):
    padding_length = length - len(strn) - 2
    left_length, right_length = (
        padding_length // 2,
        padding_length - padding_length // 2,
    )
    return f"{pattern*left_length} {strn} {pattern*right_length}"


def padded_string(strn, pattern="#", length=80):
    body_length = length - 6  # "for #___#"
    strn = strn.ljust(body_length)
    return f"#  {strn}  #"
