import tempfile
import eyed3
import os
class Music:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audiofile = eyed3.load(file_path)

    @property
    def title(self):
        return self.audiofile.tag.title if self.audiofile.tag else os.path.basename(self.file_path)

    @property
    def artist(self):
        return self.audiofile.tag.artist if self.audiofile.tag else "Unknown Artist"

    @property
    def album_cover_path(self):
        if self.audiofile.tag and self.audiofile.tag.images:
            image_data = self.audiofile.tag.images[0].image_data
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                temp_file.write(image_data)
                return temp_file.name

        # Return a default image if no album cover found
        return os.path.join("images", "album_cover.jpg")

    @property
    def duration(self):
        return self.audiofile.info.time_secs if self.audiofile.info else 0
