from collections import namedtuple
import os
import unittest
import weather

CODE_EXAM = os.path.abspath(os.path.join(__file__, "../.."))
SOURCE = os.path.dirname(os.path.realpath(__file__))
TEST_DATA = SOURCE + '/' + 'tests'
ANSWER = CODE_EXAM + '/' + 'answers' + '/'
MISSING = -9999
PATH_WX = CODE_EXAM + 'wx_data' + '/'

Day = namedtuple('Day', ['file_name', 'date', 'year', 'high', 'low', 'precip'])
Avg_Data = namedtuple('Avg_Data', ['name', 'year', 'high', 'low', 'precip'])


class WeatherTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            os.remove(ANSWER, 'MissingPrcpData.out')
            os.remove(ANSWER, 'YearlyAverages.out')
            os.remove(ANSWER, 'YearHistogram.out')
            os.remove(ANSWER, 'Correlations.out')
        except:
            open(ANSWER + 'MissingPrcpData.out', 'w')
            open(ANSWER + 'YearlyAverages.out', 'w')
            open(ANSWER + 'YearHistogram.out', 'w')
            open(ANSWER + 'Correlations.out', 'w')
        cls.c = weather.Weather()

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

    def test_get_yearly_averages(self):
        data = []
        with open(os.path.join(TEST_DATA + '/', 'USC001.txt')):
            data.extend(self.c.process_file(TEST_DATA, 'USC001.txt'))
        results = [x for x in self.c.get_yearly_averages(data) if x.year == 1989]
        expected = [
            Avg_Data(
                name='USC001.txt',
                year=1989,
                high=0.68000000000000005,
                low=-9.120000000000001,
                precip=0.60000000000000009
                )
            ]
        self.assertCountEqual(expected, results)

    def test_get_year_histogram(self):
        data = []
        results = []
        expected = [
            (1985, 1, 1, 1), (1986, 1, 1, 1), (1987, 1, 1, 1), (1988, 1, 1, 1), (1989, 1, 1, 1), (1990, 0, 0, 0),
            (1991, 0, 0, 0), (1992, 0, 0, 0), (1993, 0, 0, 0), (1994, 0, 0, 0), (1995, 0, 0, 0), (1996, 0, 0, 0),
            (1997, 0, 0, 0), (1998, 0, 0, 0), (1999, 0, 0, 0), (2000, 0, 0, 0), (2001, 0, 0, 0), (2002, 0, 0, 0),
            (2003, 0, 0, 0), (2004, 0, 0, 0), (2005, 0, 0, 0), (2006, 0, 0, 0), (2007, 0, 0, 0), (2008, 0, 0, 0),
            (2009, 0, 0, 0), (2010, 0, 0, 0), (2011, 0, 0, 0), (2012, 0, 0, 0), (2013, 0, 0, 0), (2014, 0, 0, 0)
         ]
        for file in os.listdir(TEST_DATA):
            data = []
            if file != '.DS_Store':
                data.extend(self.c.process_file(TEST_DATA, file))
                results.extend(self.c.get_yearly_averages(data))
        self.assertCountEqual(expected, self.c.get_year_histogram(results))

    def test_get_correlations(self):
        results = []
        for file in os.listdir(TEST_DATA):
            data = []
            if file != '.DS_Store':
                data.extend(self.c.process_file(TEST_DATA, file))
                results.extend(self.c.get_yearly_averages(data))
        expected = [
                ['USC001.txt', -0.19561181192180047, -0.1956118119218006, -0.19561181192180063],
                ['USC002.txt', -0.41185959065919558, -0.41185959065919542, -0.4118595906591957],
                ['USC003.txt', -0.22889302724119787, -0.22889302724119784, -0.22889302724119795],
                ['USC004.txt', -0.13797713187964089, -0.13797713187964089, -0.13797713187964095],
                ['USC005.txt', -0.084008388987234991, -0.084008388987235047, -0.084008388987235019]
            ]
        self.assertEqual(0.8660254037844386, self.c.calculate_correlation([1, 3, 4, 4], [2, 5, 5, 8])[0])
        self.assertCountEqual(expected, self.c.get_correlations(results, self.c.get_yld_data()))

