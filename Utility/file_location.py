import os
import datetime


def full_file(file_folder: list = ()) -> str:
    return os.path.abspath(os.path.join(*file_folder))


def file_date(file_name: str = "output", extension: str = " ") -> str:
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)

    file_full_name = file_name + " " + current_date_and_time_string + extension
    return file_full_name


def main():

    print(file_date("images", '.jpg'))


if __name__ == "__main__":
    main()
