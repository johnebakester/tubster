from datetime import datetime

from pony.orm import *

from db import db
from utils import utc_datetime_to_local


DATETIME_MAX_PRECISION = 6


class UploadEvent(db.Entity):
    filename = Required(unicode)
    filehash = Required(unicode)
    link = Required(unicode)
    created = Required(datetime, DATETIME_MAX_PRECISION, default=datetime.utcnow())

    class Meta:
        fields = ("filename", "filehash", "link")

    @property
    def digest(self):
        data = self.to_dict()
        del data["id"]
        data["created"] = utc_datetime_to_local(data["created"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return data

    def __str__(self):
        strn = ", ".join(f'{k}="{v}"' for k, v in self.digest.items())
        return f"{self.__class__.__name__}({strn})"

    def __repr__(self):
        return str(self)


db.generate_mapping(create_tables=True)
