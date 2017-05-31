from collections import namedtuple
import os
import unittest
import weather

DESKTOP = os.path.join(os.path.expanduser('~'), 'Desktop' + '/')
ANSWER = DESKTOP + 'answers' + '/'
MISSING = -9999
PATH_WX = DESKTOP + 'wx_data' + '/'

Day = namedtuple('Day', ['file_name', 'date', 'year', 'high', 'low', 'precip'])


class WeatherTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        try:
            os.remove(ANSWER, 'MissingPrcpData.out')
            os.remove(ANSWER, 'YearlyAverages.out')
        except:
            with open(ANSWER + 'MissingPrcpData.out', 'w') as f:
                pass
            with open(ANSWER + 'YearlyAverages.out', 'w') as f:
                pass
        self.c = weather.Weather()
        result = []
        with open(os.path.join(DESKTOP + 'wx_data' + '/', 'USC00110072.txt')):
            result.extend(self.c.process_file('USC00110072.txt'))
        self.master_list = result

    def test_read_line(self):
        expected = [Day(file_name='USC00110072.txt', date=1985, high=-22.0, low=-128.0, precip=94.0)]
        with open(os.path.join(DESKTOP + 'wx_data' + '/', 'USC00110072.txt')) as f:
            line = f.readline()
            result = self.c.convert_to_days('USC00110072.txt', line)
            self.assertEqual(expected[0].file_name, result[0].file_name)
            self.assertEqual(expected[0].date, result[0].date)
            self.assertEqual(expected[0].high, result[0].high)
            self.assertEqual(expected[0].low, result[0].low)
            self.assertEqual(expected[0].precip, result[0].precip)

    def test_process_file(self):
        result = []
        with open(os.path.join(DESKTOP + 'wx_data' + '/', 'USC00110072.txt')):
            result.extend(self.c.process_file('USC00110072.txt'))
        self.assertEqual(10865, len(result))

    def test_get_missing_precip(self):
        precips = self.c.get_missing_precip_dates(self.master_list)
        self.c.write_precip_dates(precips)
        self.assertTrue('MissingPrcpData.out' in os.listdir(ANSWER))

    def test_get_averages(self):
        expected, _ = self.c.get_averages_data(self.master_list)
        self.c.write_averages_dates(expected)
        self.assertTrue('YearlyAverages.out' in os.listdir(ANSWER))

    def test_get_year_histogram(self):
        _, file_list = self.c.get_averages_data(self.master_list)
        self.fail(self.c.get_year_histogram(file_list))
