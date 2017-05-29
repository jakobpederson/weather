import csv
import os
import unittest
import weather

MISSING = '-9999'

TEST_DATA_01 = [['1985', '2', '3', MISSING], ['1986', '3', '4', MISSING], ['1987', '4', '5', '6'], ['1988', '6', '7', '8']]

TEST_DATA_02 = [['b', 1, 2, 3, 4], ['b', 2, 3, MISSING, MISSING], ['b', 3, 4, 5, 6], ['b', 5, 6, 7, 8]]

TEST_DATA_03 = [['a', '1981', 100, 60, MISSING], ['a', '1981', 110, 50, MISSING], ['a', '1981', 120, 40, 6], ['a', '1981', 130, 30, 8]]


class WeatherTest(unittest.TestCase):

    def setUp(self):
        self.weather = weather.Weather()

    def test_count_missing_precipitation(self):
        self.assertEqual(2, self.weather.count_missing_precipitation(TEST_DATA_01))
        self.assertEqual(0, self.weather.count_missing_precipitation(TEST_DATA_02))

    def test_write_missing_precip(self):
        list_of_days = self.weather.convert_to_days('a', TEST_DATA_01)
        # list_of_days_2 = self.weather.convert_to_days(TEST_DATA_02)
        count = self.weather.count_missing_precipitation(list_of_days)
        # count_2 = self.weather.count_missing_precipitation(TEST_DATA_02)
        self.weather.write_missing_precip(list_of_days, count)
        # self.weather.write_missing_precip(list_of_days_2, count_2, app=True)
        expected = [['a', '2'], ['b', '0']]
        result = self.read_into_list_of_lists('MissingPrcpData.out')
        self.assertCountEqual(expected, result)

    def test_get_avg_max_avg_min_by_year(self):
        list_of_days = self.weather.convert_to_days(TEST_DATA_01)
        result_high, result_low = self.weather.get_max_min_by_year(list_of_days)
        self.assertEqual(2.0, result_high['1985'])
        self.assertEqual(3.0, result_high['1986'])
        self.assertEqual(4.0, result_high['1987'])
        self.assertEqual(6.0, result_high['1988'])
        self.assertEqual(3.0, result_low['1985'])
        self.assertEqual(4.0, result_low['1986'])
        self.assertEqual(5.0, result_low['1987'])
        self.assertEqual(7.0, result_low['1988'])

    def test_get_total_precip(self):
        list_of_days = self.weather.convert_to_days(TEST_DATA_01)
        self.assertEqual(6, self.weather.get_total_precip(list_of_days)['1987'])
        self.assertEqual(8, self.weather.get_total_precip(list_of_days)['1988'])

    def test_write_to_answer_2(self):
        list_of_days = self.weather.convert_to_days('a', TEST_DATA_01)
        high, low = self.weather.get_max_min_by_year(list_of_days)
        precip = self.weather.get_total_precip(list_of_days)
        result = self.weather.write_answer_2(list_of_days[0].file_name, high, low, precip)
        self.assertCountEqual(self.read_into_list_of_lists('YearlyAverages.out'), result)

    def read_into_list_of_lists(self, file_name):
        results = []
        with open(os.path.join(weather.DESKTOP + 'answers/', file_name)) as inputfile:
            for line in inputfile:
                results.append(line.strip().split('\t'))
        return results
