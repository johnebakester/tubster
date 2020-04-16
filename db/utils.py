from pony.orm import desc

from db.models import UploadEvent
from utils import get_filehash, header_string, padded_string


def get_upload_event_from_filehash(filehash):
    return (
        UploadEvent.select(lambda ue: ue.filehash == filehash)
        .order_by(desc(UploadEvent.id))
        .first()
    )


def get_link_from_file(filepath):
    filehash = get_filehash(filepath)
    ue = get_upload_event_from_filehash(filehash)
    return ue.link if ue else ""


def print_digest(obj, header="Previous record shows"):
    digest = obj.digest
    print()
    print(header_string(header, "#", 80))
    for k, v in digest.items():
        print(padded_string(f"{k} = {v}", "#", 80))
    print("#" * 80)
