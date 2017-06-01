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
        for i in range(1985, 2015):
            hi = 0.1 * numpy.mean([x.high for x in master_list if x.year == i and x.high > MISSING])
            lo = 0.1 * numpy.mean([x.low for x in master_list if x.year == i and x.low > MISSING])
            prc = 0.1 * sum([x.precip for x in master_list if x.year == i and x.precip > MISSING])
            results[i] = (
                    master_list[0][0],
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
        new_list = [item for sublist in yearly_averages for item in sublist]
        names = set([x.name for x in new_list])
        results = []
        for name in names:
            avgs = [x.high for x in new_list if x.name == name]
            if avgs:
                max_avgs = max(avgs)
                results.extend([(x.name, x.year) for x in new_list if x.high == max_avgs])
        years_maxes = []
        for i in range(1985, 2015):
            years_maxes.append((i, len([x for x in results if x[1] == i])))
        return years_maxes

        # results = []
        # new_list = [item for sublist in yearly_averages for item in sublist]
        # for i in range(1985, 2015):
        #     avg_high = [x.high for x in new_list if x.year == i and x.high > MISSING]
        #     print(avg_high)
        #     if avg_high:
        #         maximum_avg_high = max(avg_high)
        #     else:
        #         maximum_avg_high = -9999
        #     results.append([(x.name, x.year) for x in new_list if x.year == i and x.high == maximum_avg_high and x.high > -9999])


    def write_yearhistogram(self, year_histogram):
        with open(os.path.join(ANSWER, 'YearHistogram.out'), 'a') as f:
            for key, item in year_histogram:
                str_data = '{}\t{}\t{}'.format(item[0], item[1], item[3])
