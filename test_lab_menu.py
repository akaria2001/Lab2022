import unittest
import lab_menu
import getpass
import subprocess as cmd


class TestGenerateUsername(unittest.TestCase):
    def test_generate_username(self):
        """
        Test Generate Username Function
        """
        self.assertEqual(lab_menu.generate_username(), getpass.getuser())

    # Split following Unit test into seperate Unit tests

    def test_generate_menu(self):
        """
        Test Generate Menu - check it is a list
        """
        menu = lab_menu.generate_menu()
        self.assertIsInstance(menu, list)

    def test_generate_menu_item(self):
        """
        Test Generate Menu - check each item is a list
        """
        menu = lab_menu.generate_menu()
        for item in menu:
            self.assertIsInstance(item, list)

    def test_generate_menu_item_qty(self):
        """
        Test Generate Menu - check each item is a list with 3 items
        """
        menu = lab_menu.generate_menu()
        for item in menu:
            self.assertIs(len(item), 4)

    def test_generate_menu_item_1(self):
        """
        Test Generate Menu - check first item is an Integer
        """
        menu = lab_menu.generate_menu()
        for item in menu:
            self.assertIsInstance(item[0], int)

    def test_generate_menu_item_2(self):
        """
        Test Generate Menu - check second item is a string
        """
        menu = lab_menu.generate_menu()
        for item in menu:
            self.assertIsInstance(item[1], str)

    def test_generate_menu_item_3(self):
        """
        Test Generate Menu - check third item is a string
        """
        menu = lab_menu.generate_menu()
        for item in menu:
            self.assertIsInstance(item[2], str)


if __name__ == '__main__':
    cmd.call("clear", shell=False)
    print("Running Unit tests for Linux Menu Application")
    unittest.main()
