import json

from db.utils import get_link_from_file
from utils import validate_file_path


class Playlist:
    def __init__(self):
        self.data = {"items": []}
        self.default_poster = ""

    @classmethod
    def from_filepaths(cls, filepaths):
        inst = cls()
        inst.set_filepaths(filepaths)
        return inst

    def set_filepaths(self, filepaths):
        for filepath in filepaths:
            validate_file_path(filepath)
        self.filepaths = filepaths

    def make(self):
        print()
        artist = input("Enter artist name (otherwise leave blank): ") or ""
        poster = input("Enter poster image url (otherwise leave blank): ") or ""
        for filepath in self.filepaths:
            self.data["items"].append(
                self.make_item(filepath, artist=artist, poster=poster)
            )
        content = json.dumps(self.data, indent=2)
        return f"[center][tub]{content}[/tub][/center]"

    def make_item(self, filepath, artist="", poster=""):
        link = get_link_from_file(filepath)
        return {
            "title": f"{filepath.name}",
            "artist": f"{artist}",
            "src": f"{link}",
            "poster": f"{poster}",
        }
