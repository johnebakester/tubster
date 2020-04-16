from pathlib import Path

import pyperclip
from pony.orm import db_session
from pyupload.uploader.catbox import CatboxUploader

from db.models import UploadEvent
from db.utils import get_upload_event_from_filehash
from playlist import Playlist
from utils import get_filehash
from settings import SETTINGS
from uploaders import PixelDrainUploader
from db.utils import print_digest


def should_upload(filehash):
    prev_upload = get_upload_event_from_filehash(filehash)
    if prev_upload:
        print_digest(prev_upload)
        choice = input("This file was already uploaded before. Re-upload? (y/N) ")
        if choice.lower() not in ["y", "yes"]:
            print(f'Using existing link for "{prev_upload.filename}"')
            return False
    return True


def collect_filepaths(root_path):
    p = Path(root_path)
    res = []
    for filetype in SETTINGS["allowed_filetypes"]:
        res.extend(p.glob(f"**/*{filetype}"))
    return res


def print_playlist(filepaths):
    playlist = Playlist.from_filepaths(filepaths)
    data = playlist.make()
    print(data)
    try:
        pyperclip.copy(data)
    except pyperclip.PyperclipException:
        print("Could not copy playlist to clipboard.")
    return data


def get_uploader_client(filehost):
    default_uploader = PixelDrainUploader
    uploaders = {
        "pixeldrain": PixelDrainUploader,
        "catbox": CatboxUploader,
    }
    return uploaders.get(filehost, default_uploader)


@db_session
def app(source, filehost="pixeldrain"):
    filepaths = collect_filepaths(source)
    UploaderClient = get_uploader_client(filehost)
    for filepath in filepaths:
        filepath = Path(filepath)
        filehash = get_filehash(filepath)
        if should_upload(filehash):
            link = UploaderClient(filepath).execute()
            data = {
                "filehash": filehash,
                "filename": filepath.name,
                "link": link,
            }
            UploadEvent(**data)
    print_playlist(filepaths)
