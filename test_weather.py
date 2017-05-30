import csv
import os
import unittest
import weather

MISSING = '-9999'

TEST_DATA_01 = [['1985', '2', '3', MISSING], ['1986', '3', '4', MISSING], ['1987', '4', '5', '6'], ['1988', '6', '7', '8']]

TEST_DATA_02 = [['1989', MISSING, '3', MISSING], ['1990', '3', '4', '8'], ['1991', '4', '5', '6'], ['1992', '6', '7', '8']]

TEST_DATA_03 = [['a', '1981', 100, 60, MISSING], ['a', '1981', 110, 50, MISSING], ['a', '1981', 120, 40, 6], ['a', '1981', 130, 30, 8]]

TEST_DATA_04 = [
    ['USC00112348.txt',    '2006',    '155.84',    '48.34',    '75.51'],
    ['USC00112348.txt',    '2006',    '155.84',    '41.11',    '75.51'],
    ['USC00112348.txt',    '2006',    '155.84',    '24.34',    '33.08'],
    ['USC00112348.txt',    '2006',    '151.87',    '39.59',    '-816.72'],
    ['USC00112348.txt',    '2010',    '-9999.00',    '-9999.00',    '-9999.00'],
    ['USC00112348.txt',    '2011',    '145.05',    '22.44',    '-7704.15'],
    ['USC00112348.txt',    '2012',    '189.46',    '64.93',    '-9999.00'],
    ['USC00112348.txt',    '2013',    '-9999.00',    '-9999.00',    '-9999.00'],
    ['USC00112348.txt',    '2014',    '171.65',    '71.66',    '-576.98']
]


class WeatherTest(unittest.TestCase):

    def setUp(self):
        self.weather = weather.Weather()
        try:
            os.remove(weather.DESKTOP + 'answers/' + 'MissingPrcpData.out')
            os.remove(weather.DESKTOP + 'answers/' + 'YearlyAverages.out')
        except:
            pass

    def test_count_missing_precipitation(self):
        list_of_days = self.weather.convert_to_days('a', TEST_DATA_01)
        self.assertEqual(2, self.weather.count_missing_precipitation(list_of_days))
        list_of_days = self.weather.convert_to_days('b', TEST_DATA_02)
        self.assertEqual(0, self.weather.count_missing_precipitation(list_of_days))

    def test_write_missing_precip(self):
        list_of_days = self.weather.convert_to_days('a', TEST_DATA_01)
        list_of_days_2 = self.weather.convert_to_days('b', TEST_DATA_02)
        count = self.weather.count_missing_precipitation(list_of_days)
        count_2 = self.weather.count_missing_precipitation(list_of_days_2)
        self.weather.write_missing_precip(list_of_days, count)
        self.weather.write_missing_precip(list_of_days_2, count_2)
        expected = [['a', '2'], ['b', '0']]
        result = self.read_into_list_of_lists('MissingPrcpData.out')
        self.assertCountEqual(expected, result)

    def test_get_avg_max_avg_min_by_year(self):
        list_of_days = self.weather.convert_to_days('a', TEST_DATA_01)
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
        list_of_days = self.weather.convert_to_days('a', TEST_DATA_01)
        self.assertEqual(6, self.weather.get_total_precip(list_of_days)['1987'])
        self.assertEqual(8, self.weather.get_total_precip(list_of_days)['1988'])

    def test_write_to_answer_2(self):
        list_of_days = self.weather.convert_to_days('a', TEST_DATA_01)
        high, low = self.weather.get_max_min_by_year(list_of_days)
        precip = self.weather.get_total_precip(list_of_days)
        result = self.weather.write_answer_2(list_of_days[0].file_name, high, low, precip)
        self.assertCountEqual(self.read_into_list_of_lists('YearlyAverages.out'), result)

    def test_count_all(self):
        expected = (
            {'2014': 1, '2011': 1, '2012': 1, '2006': 3},
            {'2014': 1, '2011': 1, '2012': 1, '2006': 1},
            {'2014': 1, '2011': 1, '2006': 2}
         )
        self.assertCountEqual(expected, self.weather.count_all(TEST_DATA_04))

    def text_x(self):
        self.fail(self.weather.pearson(TEST_DATA_04))

    def read_into_list_of_lists(self, file_name):
        results = []
        with open(os.path.join(weather.DESKTOP + 'answers/', file_name)) as inputfile:
            for line in inputfile:
                results.append(line.strip().split('\t'))
        return results
