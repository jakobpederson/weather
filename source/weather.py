from collections import namedtuple, defaultdict, Counter
import math
import numpy
import os

CODE_EXAM = os.path.abspath(os.path.join(__file__, "../.."))
SOURCE = os.path.dirname(os.path.realpath(__file__))
ANSWER = CODE_EXAM + '/' + 'answers' + '/'
MISSING = -9999
Day = namedtuple('Day', ['file_name', 'date', 'year', 'high', 'low', 'precip'])
Avg_Data = namedtuple('Avg_Data', ['name', 'year', 'high', 'low', 'precip'])
MISSING = -9999


class Weather():

    def convert_to_days(self, file, line):
        value = line.split('\t')
        return [
            Day(
                file_name=file,
                date=int(value[0]),
                year=int(value[0][:4].strip()),
                high=float(value[1].strip()),
                low=float(value[2].strip()),
                precip=float(value[3].strip())
            )
        ]

    def process_file(self, path, file):
        result = []
        with open(os.path.join(path + '/', file)) as f:
            for line in f:
                result.extend(self.convert_to_days(file, line))
        return result

    def get_missing_prcp_data(self, file_list):
        results = Counter(
            [x.file_name for x in file_list if x.high > MISSING and x.low > MISSING and x.precip == MISSING]
        )
        self.write_missingprcpdata(results)
        return results

    def write_missingprcpdata(self, results):
        with open(os.path.join(ANSWER, 'MissingPrcpData.out'), 'a') as f:
            for key, item in results.items():
                str_data = '{}\t{}'.format(key, item)
                f.write(str_data + '\n')
        return results

    def get_yearly_averages(self, master_list):
        results = defaultdict(lambda: ('x', 1, -9999, -9999, -9999))
        if not master_list:
            return
        for i in range(1985, 2015):
            hi = 0.1 * numpy.mean([x.high for x in master_list if x.year == i and x.high > MISSING])
            lo = 0.1 * numpy.mean([x.low for x in master_list if x.year == i and x.low > MISSING])
            prc = 0.1 * sum([x.precip for x in master_list if x.year == i and x.precip > MISSING])
            results[i] = (
                    master_list[0].file_name,
                    i,
                    hi if not math.isnan(hi) else -9999,
                    lo if not math.isnan(lo) else -9999,
                    prc if prc != 0 else -9999,
                )
        self.write_yearlyaverages(results)
        return [Avg_Data(name=x[0], year=x[1], high=x[2], low=x[3], precip=x[4]) for x in results.values()]

    def write_yearlyaverages(self, results):
        with open(os.path.join(ANSWER, 'YearlyAverages.out'), 'a') as f:
            for year, item in results.items():
                str_data = '{}\t{}\t{:0.2f}\t{:0.2f}\t{:0.2f}'.format(item[0], year, item[2], item[3], item[4])
                f.write(str_data + '\n')
        return results

    def get_year_histogram(self, yearly_averages):
        answer = []
        results = []
        for name in set([x.name for x in yearly_averages]):
            files_by_name = [x for x in yearly_averages if x.name == name]
            max_by_file = max([x.high for x in files_by_name])
            answer.extend([(x.name, x.year) for x in files_by_name if x.high == max_by_file])
        for i in range(1985, 2015):
            results.append((i, len([x for x in answer if x[1] == i])))
        return results

        # new_list = [item for sublist in yearly_averages for item in sublist]
        # names = set([x.name for x in new_list])
        # results = []
        # results_low = []
        # results_precip = []
        # for name in names:
        #     avgs = [x.high for x in new_list if x.name == name]
        #     avgs_low = [x.low for x in new_list if x.name == name]
        #     avgs_prc = [x.precip for x in new_list if x.name == name]
        #     if avgs:
        #         max_avgs = max(avgs)
        #         results.extend([(x.name, x.year) for x in new_list if x.high == max_avgs])
        #     if avgs:
        #         min_avgs = min(avgs_low)
        #         results_low.extend([(x.name, x.year) for x in new_list if x.low == min_avgs])
        #     if avgs:
        #         max_prc_avgs = max(avgs_prc)
        #         results_precip.extend([(x.name, x.year) for x in new_list if x.precip == max_prc_avgs])
        # years_maxes = {}
        # years_lows = {}
        # years_precips = {}
        # for i in range(1985, 2015):
        #     years_maxes[i] = len([x for x in results if x[1] == i])
        #     years_lows[i] = len([x for x in results_low if x[1] == i])
        #     years_precips[i] = len([x for x in results_precip if x[1] == i])
        # self.write_yearhistogram(years_maxes, years_lows, years_precips)
        # return years_maxes, years_lows, years_precips

    def write_yearhistogram(self, year_maxes, year_lows, year_precips):
        with open(os.path.join(ANSWER, 'YearHistogram.out'), 'a') as f:
            for i in range(1985, 2015):
                str_data = '{}\t{}\t{}\t{}'.format(i, year_maxes[i], year_lows[i], year_precips[i])
                f.write(str_data + '\n')
            return []

if __name__ == '__main__':
    c = Weather()
    yearly_avg = []
    try:
        os.remove(CODE_EXAM + '/wx_data' + '/', 'MissingPrcpData.out')
        os.remove(CODE_EXAM + '/wx_data' + '/', 'YearlyAverages.out')
        os.remove(CODE_EXAM + '/wx_data' + '/', 'YearHistogram.out')
    except:
        pass
    file1 = open(CODE_EXAM + '/wx_data' + '/' + 'MissingPrcpData.out', 'w')
    file2 = open(CODE_EXAM + '/wx_data' + '/' + 'YearlyAverages.out', 'w')
    file3 = open(CODE_EXAM + '/wx_data' + '/' + 'YearHistogram.out', 'w')
    results = []
    for file in os.listdir(CODE_EXAM + '/wx_data' + '/'):
        if file != 'DS_Store':
            file_data = c.process_file(CODE_EXAM + '/wx_data' + '/', file)
            c.get_missing_prcp_data(file_data)
            data = c.get_yearly_averages(file_data)
            if data:
                results.extend(c.get_yearly_averages(file_data))
    c.get_year_histogram(results)
