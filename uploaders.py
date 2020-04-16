from pyupload.uploader.base import Uploader


class PixelDrainUploader(Uploader):
    def __init__(self, filename):
        self.filename = filename
        self.file_host_url = "https://pixeldrain.com/api/file"

    def execute(self):
        file = open(self.filename, "rb")
        with open(self.filename, "rb") as f:
            data = {
                "name": f"{file.name}",
                "anonymous": "true",
                "file": (file.name, f, self._mimetype()),
            }
            response = self._multipart_post(data)
        data = response.json()
        if not data:
            raise Exception("PixelDrain did not return JSON response.")
        return f'https://pixeldrain.com/api/file/{data["id"]}'
