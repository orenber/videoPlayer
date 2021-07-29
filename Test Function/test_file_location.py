from unittest import TestCase
from Utility.file_location import file_date, full_file, create_folder_if_not_exist
import os

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

    def test_create_folder_if_not_exist(self):
        test_path = ["Resources", "images", "faces", "Oren"]
        path = full_file(test_path)
        path_exist = create_folder_if_not_exist(path)
        self.assertTrue(path_exist, "directory created in " + path)
        test_path_create = ["Resources", "images", "faces", "Jhon"]
        path_to_create = full_file(test_path_create)
        create_path = create_folder_if_not_exist(path_to_create)
        self.assertTrue(create_path, "directory created in " + path)
        os.rmdir(path_to_create)








