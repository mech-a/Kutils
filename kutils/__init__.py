import logging
import json

# print('__init__ is executed before __main__ when calling -m kutils')
logging.warning("You've imported Kutils, which is intended to be ran via the command line.")


class Configuration:
    file_path = None
    google_credentials = []
    twitter_credentials = []
    twitter_link_sheet = None
    youtube_link_sheet = None

    def write(self, f_path):
        with open(f_path, 'w') as json_file:
            json.dump(self.file_path, json_file)
            json.dump(self.google_credentials, json_file)
            json.dump(self.twitter_credentials, json_file)
            json.dump(self.twitter_link_sheet, json_file)
            json.dump(self.youtube_link_sheet, json_file)

    @staticmethod
    def read(f_path):
        with open(f_path, 'r') as json_file:
            with json.load(json_file) as json_obj:
                # json.dump(self.file_path, json_file)
                # json.dump(self.google_credentials, json_file)
                # json.dump(self.twitter_credentials, json_file)
                # json.dump(self.twitter_link_sheet, json_file)
                # json.dump(self.youtube_link_sheet, json_file)
                print(json_obj)



class Executor:
    def get_dead_youtube_cells_from_sheet(self):
        return



