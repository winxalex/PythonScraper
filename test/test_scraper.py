import unittest
from unittest.mock import patch
from scrapers.scraper import parse_html,get_driver
from storages.storage import create_connection


class TestParseFunction(unittest.TestCase):



    @patch('scrapers.scraper.get_load_time')
    def setUp(self, mock_get_load_time):
        mock_get_load_time.return_value = 'mocked!'
        with open('test.html', encoding='utf-8') as f:
            html = f.read()
            self.output = parse_html(html)
        self.driver_url="D:\Projects\PythonScraper\chromedriver.exe"
        self.db_url= r"D:\Projects\PythonScraper\scrapped.db"


    def tearDown(self):
        self.output = []

    def test_output_is_not_none(self):
        self.assertIsNotNone(self.output)

    def test_output_is_a_list(self):
        self.assertTrue(isinstance(self.output, list))

    def test_output_is_a_list_of_string(self):
        self.assertTrue(all(isinstance(elem, str) for elem in self.output))

    def test_brower(self):
        browser=get_driver(self.driver_url)
        self.assertTrue(browser is not None)

    def test_db(self):
        conn=create_connection(self.db_url)
        self.assertTrue(conn is not None)
        conn.close()


if __name__ == '__main__':
    unittest.main()
