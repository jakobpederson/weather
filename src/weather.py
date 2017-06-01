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
            hi = self.get_average_if_len_gt_zero([x.high for x in master_list if x.year == i and x.high > MISSING])
            lo = self.get_average_if_len_gt_zero([x.low for x in master_list if x.year == i and x.low > MISSING])
            prc = self.get_average_if_len_gt_zero([x.precip for x in master_list if x.year == i and x.precip > MISSING])
            results[i] = (
                    master_list[0].file_name,
                    i,
                    hi,
                    lo,
                    prc if prc != 0 else -9999,
                )
        self.write_yearlyaverages(results)
        return [Avg_Data(name=x[0], year=x[1], high=x[2], low=x[3], precip=x[4]) for x in results.values()]

    def get_average_if_len_gt_zero(self, data):
        if len(data) > 0:
            return 0.1 * numpy.mean(data)
        return -9999

    def write_yearlyaverages(self, results):
        with open(os.path.join(ANSWER, 'YearlyAverages.out'), 'a') as f:
            for year, item in results.items():
                str_data = '{}\t{}\t{:0.2f}\t{:0.2f}\t{:0.2f}'.format(item[0], year, item[2], item[3], item[4])
                f.write(str_data + '\n')
        return results

    def get_year_histogram(self, yearly_averages):
        answer = []
        answer_low = []
        answer_precip = []
        results = []
        for name in set([x.name for x in yearly_averages]):
            files_by_name = [x for x in yearly_averages if x.name == name]
            high_by_file = max([x.high for x in files_by_name])
            low_by_file = min([x.low for x in files_by_name if x.low > MISSING])
            precip_by_file = max([x.precip for x in files_by_name])
            answer.extend([(x.name, x.year) for x in files_by_name if x.high == high_by_file])
            answer_low.extend([(x.name, x.year) for x in files_by_name if x.low == low_by_file])
            answer_precip.extend([(x.name, x.year) for x in files_by_name if x.precip == precip_by_file])
        for i in range(1985, 2015):
            results.append((i, len([x for x in answer if x[1] == i]), len([x for x in answer_low if x[1] == i]), len([x for x in answer_precip if x[1] == i])))
        self.write_yearhistogram(results)
        return results

    def write_yearhistogram(self, results):
        with open(os.path.join(ANSWER, 'YearHistogram.out'), 'a') as f:
            for result in results:
                str_data = '{}\t{}\t{}\t{}'.format(result[0], result[1], result[2], result[3])
                f.write(str_data + '\n')
            return []

    def start_up(self):
        try:
            os.remove(CODE_EXAM + '/answers' + '/', 'MissingPrcpData.out')
            os.remove(CODE_EXAM + '/answers' + '/', 'YearlyAverages.out')
            os.remove(CODE_EXAM + '/answers' + '/', 'YearHistogram.out')
        except:
            pass
        file1 = open(CODE_EXAM + '/answers' + '/' + 'MissingPrcpData.out', 'w')
        file2 = open(CODE_EXAM + '/answers' + '/' + 'YearlyAverages.out', 'w')
        file3 = open(CODE_EXAM + '/answers' + '/' + 'YearHistogram.out', 'w')
        return file1, file2, file3

    def get_correlations(self, results, yld_data):
        answers = []
        for file in set([x.name for x in results]):
            weather_station = [(x.high, x.low, x.precip) for x in results if x.name == file]
            answers.append(
                [
                    file,
                    self.calculate_correlation([x[0] for x in weather_station], yld_data)[0],
                    self.calculate_correlation([x[1] for x in weather_station], yld_data)[0],
                    self.calculate_correlation([x[2] for x in weather_station], yld_data)[0]
                ]
            )
        self.write_correlations(answers)
        return answers

    def calculate_correlation(self, x, y):
        from scipy.stats.stats import pearsonr
        return pearsonr(x, y)

    def get_yld_data(self):
        data = []
        with open(os.path.join(CODE_EXAM + '/yld_data/' + 'US_corn_grain_yield.txt')) as f:
            for line in f:
                data.append(float(line.strip().split('\t')[1]))
        return data

    def write_correlations(self, answers):
        result = []
        with open(os.path.join(CODE_EXAM + '/answers/',  'Correlations.out'), 'a') as f:
            for answer in answers:
                string_data = '{}\t{:0.2f}\t{:0.2f}\t{:0.2f}\t'.format(
                    answer[0],
                    answer[1],
                    answer[2],
                    answer[3],
                )
                result.append(string_data.strip('\t'))
            for value in sorted(set(result)):
                f.write(value + '\n')

if __name__ == '__main__':
    c = Weather()
    c.start_up()
    yearly_avg = []
    results = []
    for file in os.listdir(CODE_EXAM + '/wx_data' + '/'):
        if file != '.DS_Store':
            file_data = c.process_file(CODE_EXAM + '/wx_data' + '/', file)
            c.get_missing_prcp_data(file_data)
            data = c.get_yearly_averages(file_data)
            if data:
                results.extend(c.get_yearly_averages(file_data))
    c.get_year_histogram(results)
    c.get_correlations(results, c.get_yld_data())
