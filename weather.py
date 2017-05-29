from collections import namedtuple, defaultdict
import os
from argparse import ArgumentParser

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop/")

Day = namedtuple('Day', ['file_name', 'date', 'high', 'low', 'precip'])
MISSING = -9999


class Weather():

    def convert_to_days(self, filename, list_of_lists):
        result = []
        for value in list_of_lists:
            result.append(Day(file_name=filename, date=(value[0].strip()), high=float((value[1].strip())), low=float((value[2].strip())), precip=(value[3].strip())))
        return result

    def count_missing_precipitation(self, list_of_days):
        count = 0
        for day in list_of_days:
            if day.high > MISSING and day.low > MISSING and day.precip == MISSING:
                count += 1
        return count

    def write_missing_precip(self, list_of_days, count):
        answer = DESKTOP + 'answers/'


        # if app:
        #     with open(os.path.join(answer, 'MissingPrcpData.out'), 'a') as f:
        #         f.write(list_of_days[0].file_name + "\t" + str(count) + '\n')

        # else:
        with open(os.path.join(answer, 'MissingPrcpData.out'), 'a') as f:
            f.write(list_of_days[0].file_name + "\t" + str(count) + '\n')

    def get_max_min_by_year(self, list_of_days):
        years_high = defaultdict(list)
        years_low = defaultdict(list)
        for day in list_of_days:
            if day.high > MISSING:
                years_high[day.date[:4]].append(float(day.high))
            if day.low > MISSING:
                years_low[day.date[:4]].append(float(day.low))
        return self.get_averages(years_high, years_low)

    def get_averages(self, years_high, years_low):
        high_avg = defaultdict(lambda: float(-9999))
        low_avg = defaultdict(lambda: float(-9999))
        for i in range(1985, 2015):
            key = str(i)
            if len(years_high[key]) > 0:
                high_avg[key] = sum(years_high[key])/len(years_high[key])
            if len(years_low[key]) > 0:
                low_avg[key] = sum(years_low[key])/len(years_low[key])
        return high_avg, low_avg

    def get_total_precip(self, list_of_days):
        total_precip = defaultdict(list)
        final_precip = defaultdict(int)
        for day in list_of_days:
            total_precip[day.date[:4]].append(float(day.precip))
        for i in range(1985, 2015):
            key = str(i)
            if total_precip[key]:
                final_precip[key] = sum(total_precip[key])/len(total_precip[key])
            else:
                final_precip[key] = MISSING
        return final_precip

    def write_answer_2(self, file_name, high_avg, low_avg, total_precip):
        result = []
        with open(os.path.join(DESKTOP + 'answers', 'YearlyAverages.out'), 'a') as f:
            for i in range(1985, 2015):
                key = str(i)
                string_data = '{}\t{}\t{:0.2f}\t{:0.2f}\t{:0.2f}'.format(file_name, key, high_avg[key], low_avg[key], total_precip[key])
                f.write(string_data + '\n')
                result.append(string_data.split('\t'))
        return result


if __name__ == "__main__":
    path_wx_data = DESKTOP + 'wx_data/'
    path_yld_data = DESKTOP + 'yld_data/'
    try:
        os.remove(DESKTOP + 'answers/' + 'YearlyAverages.out')
        os.remove(DESKTOP + 'answers/' + 'MissingPrcpData.out')
    except:
        pass
    g = Weather()
    for filename in os.listdir(path_wx_data):
        data = []
        new_data = []
        with open(os.path.join(path_wx_data, filename)) as inputfile:
            for line in inputfile:
                data.append(line.strip().split('\t'))
            list_of_days = g.convert_to_days(filename, data)
            count = g.count_missing_precipitation(list_of_days)
            g.write_missing_precip(list_of_days, count)
            high, low = g.get_max_min_by_year(list_of_days)
            precip = g.get_total_precip(list_of_days)
            g.write_answer_2(filename, high, low, precip)
