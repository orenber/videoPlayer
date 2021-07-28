from Utility.file_location import *


class LOGGER(object):

    def __int__(self, app_name: str = "App"):

        path_log = full_file(['Logger', app_name])
        create_folder_if_not_exist(path_log)

        logging.basicConfig(level=logging.INFO, filename=file_date(app_name, '.log'), filemode='w')
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



