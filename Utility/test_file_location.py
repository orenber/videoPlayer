from unittest import TestCase
from file_location import file_date


class Test(TestCase):
    def test_file_date(self):
        file_name = file_date("file_name", '.text')
        print(file_name)
        obj = open(file_name, "w+")
        obj.close()
        self.assertEqual(file_name, 'file_name.txt')

