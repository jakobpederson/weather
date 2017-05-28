import csv
import os
import unittest
import weather

MISSING = -9999

TEST_DATA_01 = [['a', '1981', 2, 3, MISSING], ['a', '1982', 3, 4, MISSING], ['a', '1983', 4, 5, 6], ['a', '1984', 6, 7, 8]]

TEST_DATA_02 = [['b', 1, 2, 3, 4], ['b', 2, 3, MISSING, MISSING], ['b', 3, 4, 5, 6], ['b', 5, 6, 7, 8]]

TEST_DATA_03 = [['a', '1981', 100, 60, MISSING], ['a', '1981', 110, 50, MISSING], ['a', '1981', 120, 40, 6], ['a', '1981', 130, 30, 8]]


class WeatherTest(unittest.TestCase):

    def setUp(self):
        self.weather = weather.Weather()

    def test_count_missing_precipitation(self):
        self.assertEqual(2, self.weather.count_missing_precipitation(TEST_DATA_01))
        self.assertEqual(0, self.weather.count_missing_precipitation(TEST_DATA_02))

    def test_write_missing_precip(self):
        count = self.weather.count_missing_precipitation(TEST_DATA_01)
        count_2 = self.weather.count_missing_precipitation(TEST_DATA_02)
        list_of_days = self.weather.convert_to_days(TEST_DATA_01)
        list_of_days_2 = self.weather.convert_to_days(TEST_DATA_02)
        self.weather.write_missing_precip(list_of_days, count)
        self.weather.write_missing_precip(list_of_days_2, count_2)
        expected = [['a', '2'], ['b', '0']]
        result = self.read_into_list_of_lists('MissingPrcpData.out')
        self.assertCountEqual(expected, result)

    def test_get_max_min_by_year(self):
        list_of_days = self.weather.convert_to_days(TEST_DATA_01)
        result = self.weather.get_max_min_by_year(list_of_days)
        self.assertTrue(result['high']['1981'] == 2)
        self.assertTrue(result['low']['1981'] == 3)
        self.assertTrue(result['high']['1982'] == 3)
        self.assertTrue(result['low']['1982'] == 4)
        self.assertTrue(result['high']['1983'] == 4)
        self.assertTrue(result['low']['1983'] == 5)
        self.assertTrue(result['high']['1984'] == 6)
        self.assertTrue(result['low']['1984'] == 7)
        list_of_days = self.weather.convert_to_days(TEST_DATA_03)
        result = self.weather.get_max_min_by_year(list_of_days)
        self.assertTrue(result['high']['1981'] == 130)
        self.assertTrue(result['low']['1981'] == 30)

    def read_into_list_of_lists(self, file_name):
        results = []
        with open(os.path.join(weather.DESKTOP, file_name)) as inputfile:
            for line in inputfile:
                results.append(line.strip().split('\t'))
        return results
