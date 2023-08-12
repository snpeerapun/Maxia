import os

class Utility:
    @staticmethod
    def find_files(folder, extension):
        found_files = []

        for entry in os.scandir(folder):
            if entry.is_file() and entry.name.endswith(extension):
                found_files.append(entry.path)
            elif entry.is_dir():
                found_files.extend(Utility.find_files(entry.path, extension))

        return found_files