import os.path

from Utility.file_location import *
import logging


def setup_logger(app_name: str):
    path_log = full_file(['Logger', app_name])
    create_folder_if_not_exist(path_log)
    file_path = os.path.join(path_log, file_date(app_name, '.log'))

    logging.basicConfig(level=logging.INFO, filename=file_path, filemode='w',
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    log = logging.getLogger(app_name+"Start")
    log.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # add ch to logger
    log.addHandler(ch)
    log.info("Start: " + app_name)
    return log


def main():
    log = setup_logger('test_log')
    log.warning('this is warning')


if __name__ == "__main__":
    main()
