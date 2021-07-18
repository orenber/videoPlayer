from unittest import TestCase
from Utility.file_location import *


class Test(TestCase):
    def test_file_date(self):
        file_name = file_date("test_file_date", '.txt')
        print(file_name)
        obj = open(file_name, "w+")
        obj.close()
        self.assertRegexpMatches(file_name, 'test_file_date', '*.txt')

    def test_full_file(self):
        test_path = ["Resources", "images", "301-F.jpg"]
        path = full_file(test_path)
        self.assertEqual(path, os.path.abspath(os.path.join(os.pardir, *test_path)),
                         'file path name are not the same :-(')
