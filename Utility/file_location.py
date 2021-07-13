import os
import logging
from datetime import datetime


def full_file(file_folder: list = ()) -> str:
    return os.path.abspath(os.path.join(*file_folder))


def file_date(file_name: str = "output", extension: str = " ") -> str:

    current_date_and_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    current_date_and_time_string = str(current_date_and_time)

    file_full_name = file_name + "_" + current_date_and_time_string + extension
    return file_full_name


class LOGGER:
    def __int__(self, app_name: str):
        logging.basicConfig(level=logging.INFO, filename= file_date(app_name, '.log'), filemode='w')
        self.logger = logging.getLogger(app_name+"Start")
        self.logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

def main():

    print(file_date("images", '.jpg'))


if __name__ == "__main__":
    main()
