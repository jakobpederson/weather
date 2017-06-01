from collections import namedtuple
import os
import sys
import unittest
import weather

CODE_EXAM = os.path.abspath(os.path.join(__file__, "../.."))
SOURCE = os.path.dirname(os.path.realpath(__file__))
TEST_DATA = SOURCE + '/' + 'tests'
ANSWER = CODE_EXAM + '/' + 'answers'
MISSING = -9999
PATH_WX = CODE_EXAM + 'wx_data' + '/'
FILE_LIST = [
    'UC001.txt',
    'UC002.txt',
    'UC003.txt',
    'UC004.txt',
    'UC005.txt',
    ]

Day = namedtuple('Day', ['file_name', 'date', 'year', 'high', 'low', 'precip'])


class WeatherTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        try:
            os.remove(ANSWER, 'MissingPrcpData.out')
            os.remove(ANSWER, 'YearlyAverages.out')
            os.remove(ANSWER, 'YearHistogram.out')
        except:
            open(ANSWER + 'MissingPrcpData.out', 'w')
            open(ANSWER + 'YearlyAverages.out', 'w')
            open(ANSWER + 'YearHistogram.out', 'w')
        self.c = weather.Weather()

    def test_read_line(self):
        expected = [Day(file_name='USC001.txt', date=19890101, year=1989, high=56.0, low=-50.0, precip=0.0)]
        with open(os.path.join(TEST_DATA + '/', 'USC001.txt')) as f:
            line = f.readline()
            result = self.c.convert_to_days('USC001.txt', line)
            self.assertEqual(expected[0].file_name, result[0].file_name)
            self.assertEqual(expected[0].date, result[0].date)
            self.assertEqual(expected[0].high, result[0].high)
            self.assertEqual(expected[0].low, result[0].low)
            self.assertEqual(expected[0].precip, result[0].precip)

    def test_process_file(self):
        results = []
        expected = [
            Day(file_name='USC001.txt', date=19890101, year=1989, high=56.0, low=-50.0, precip=0.0),
            Day(file_name='USC001.txt', date=19890102, year=1989, high=11.0, low=-56.0, precip=0.0),
            Day(file_name='USC001.txt', date=19890103, year=1989, high=-33.0, low=-111.0, precip=0.0),
            Day(file_name='USC001.txt', date=19890104, year=1989, high=-17.0, low=-133.0, precip=30.0),
            Day(file_name='USC001.txt', date=19890105, year=1989, high=17.0, low=-106.0, precip=0.0)
         ]
        with open(os.path.join(TEST_DATA + '/', 'USC001.txt')):
            results.extend(self.c.process_file(TEST_DATA, 'USC001.txt'))
        self.assertEqual(5, len(results))
        for result in results:
            self.assertTrue(result in expected)

    def test_get_missing_prcp_data(self):
        data = []
        with open(os.path.join(TEST_DATA + '/', 'USC002.txt')):
            data.extend(self.c.process_file(TEST_DATA, 'USC002.txt'))
        results = self.c.get_missing_prcp_data(data)
        self.assertTrue('USC002.txt' in results.keys())
        self.assertTrue(1 in results.values())
        self.assertTrue('MissingPrcpData.out' in os.listdir(ANSWER))

    def test_get_yearly_averages(self):
        data = []
        with open(os.path.join(TEST_DATA + '/', 'USC001.txt')):
            data.extend(self.c.process_file(TEST_DATA, 'USC001.txt'))
        results = self.c.get_yearly_averages(data)
        self.assertTrue(results[1989] == ('USC001.txt', 1989, 0.68000000000000005, -9.120000000000001, 3.0))
        self.assertTrue('YearlyAverages.out' in os.listdir(ANSWER))

    def test_get_year_histogram(self):
        data = []
        results = []
        expected = {1985: 1, 1986: 1, 1987: 1, 1988: 1, 1989: 1, 1990: 0, 1991: 0, 1992: 0, 1993: 0, 1994: 0, 1995: 0, 1996: 0, 1997: 0, 1998: 0, 1999: 0, 2000: 0, 2001: 0, 2002: 0,2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0,2013: 0, 2014: 0}, {1985: 20, 1986: 20, 1987: 20, 1988: 20, 1989: 20, 1990: 25, 1991: 25,1992: 25, 1993: 25, 1994: 25, 1995: 25, 1996: 25, 1997: 25, 1998: 25, 1999: 25, 2000: 25,2001: 25, 2002: 25, 2003: 25, 2004: 25, 2005: 25, 2006: 25, 2007: 25, 2008: 25, 2009: 25,2010: 25, 2011: 25, 2012: 25, 2013: 25, 2014: 25}, {1985: 1, 1986: 1, 1987: 1, 1988: 1, 1989: 1, 1990: 0, 1991: 0, 1992: 0, 1993: 0, 1994: 0, 1995: 0, 1996: 0, 1997: 0, 1998: 0, 1999: 0, 2000: 0, 2001: 0, 2002: 0, 2003: 0, 2004: 0, 2005: 0, 2006: 0, 2007: 0, 2008: 0, 2009: 0, 2010: 0, 2011: 0, 2012: 0, 2013: 0, 2014: 0}
        for file in os.listdir(TEST_DATA):
            data = []
            if file != '.DS_Store':
                data.extend(self.c.process_file(TEST_DATA, file))
                results.append(self.c.get_yearly_averages(data))
        self.assertCountEqual(expected, self.c.get_year_histogram(results))
