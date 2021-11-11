from unittest import TestCase
from Utility.logger_setup import setup_logger


class TestLOGGER(TestCase):

    def setUp(self):
        self.logger = setup_logger("APP_TEST")

        pass

    def test__init__(self):
        pass
