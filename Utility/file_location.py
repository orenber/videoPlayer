import os
from datetime import datetime


def full_file(file_folder: list = ()) -> str:
    return os.path.abspath(os.path.join(os.pardir, *file_folder))


def file_date(file_name: str = "output", extension: str = " ") -> str:

    current_date_and_time = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    current_date_and_time_string = str(current_date_and_time)

    file_full_name = file_name + "_" + current_date_and_time_string + extension
    return file_full_name


def create_folder_if_not_exist(file_folder: str = os.pardir) -> bool:

    os.makedirs(file_folder, exist_ok=True)
    is_exist = os.path.isdir(file_folder)
    return is_exist


def main():

    print(file_date("images", '.jpg'))


if __name__ == "__main__":
    main()
