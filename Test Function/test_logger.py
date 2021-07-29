from unittest import TestCase
from Utility.logger import LOGGER


class TestLOGGER(TestCase):

    def setUp(self):
        self.logger = LOGGER("APP_TEST")

        pass

    def test__init__(self):
        pass
