from collections import namedtuple, defaultdict, Counter
import numpy
import os

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop/")
ANSWER = DESKTOP + 'answers' + '/'

Day = namedtuple('Day', ['file_name', 'date', 'year', 'high', 'low', 'precip'])
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

    def process_file(self, file):
        result = []
        with open(os.path.join(DESKTOP + 'wx_data' + '/', file)) as f:
            for line in f:
                result.extend(self.convert_to_days(file, line))
        return result

    def get_weather_data(self):
        result = []
        for file in os.listdir(DESKTOP + 'wx_data' + '/'):
            with open(os.path.join(DESKTOP + 'wx_data' + '/', file)) as f:
                for line in f:
                    result.extend(self.convert_to_days(file, line))
        return result

    def get_missing_precip_dates(self, file_list):
        return Counter([x.file_name for x in file_list if x.high > MISSING and x.low > MISSING and x.precip == MISSING])

    def write_precip_dates(self, precips):
        with open(os.path.join(ANSWER, 'MissingPrcpData.out'), 'a') as f:
            for key, item in precips.items():
                str_data = '{}\t{}'.format(key, item)
                f.write(str_data + '\n')
        return precips

    Avg_Data = namedtuple('Avg_Data', ['name', 'year', 'high', 'low', 'precip'])

    def get_averages_data(self, master_list):
        result = defaultdict(lambda: float(-9999))
        for i in range(1985, 2015):
            result[i] = (
                self.Avg_Data(
                    name=master_list[0][0], year=i,  high=10 * numpy.mean([x.high for x in master_list if x.year == i and x.high > MISSING]),
                    low=10 * numpy.mean([x.low for x in master_list if x.year == i and x.low > MISSING]),
                    precip=10 * sum([x.precip for x in master_list if x.year == i and x.precip > MISSING]),
                )
            )
        return result

    def write_averages_dates(self, result):
        with open(os.path.join(ANSWER, 'YearlyAverages.out'), 'w') as f:
            for key, item in result.items():
                str_data = '{}\t{}\t{:0.2f}\t{:0.2f}\t{:0.2f}'.format(item.name, key, item.high, item.low, item.precip)
                f.write(str_data + '\n')
        return result

    def get_year_histogram(self, file_list):
        result = []
        for i in range(1985, 2015):
            result.append((file_list[1985][0], i, max([x.high for x in file_list.values() if x.year == i])))
        return result


    #         high = [(x.file_name, x.high) for x in master_list if x.date == i and x.high > -MISSING]
    #         low = [(x.file_name, x.low) for x in master_list if x.date == i and x.low > MISSING]
    #         precip = [(x.file_name, x.precip) for x in master_list if x.precip > MISSING]
    #         names_high = set([x[0] for x in high])
    #         names_low = set([x[0] for x in low])
    #         names_precip = set([x[0] for x in precip])
    #         result_high = defaultdict(lambda: float(MISSING))
    #         result_low = defaultdict(lambda: float(MISSING))
    #         result_precip = defaultdict(lambda: float(MISSING))
    #         result = {}
    #         for j in names_high:
    #             result_high[j] = numpy.mean([x[1] for x in high if x[0] == j])
    #         for j in names_low:
    #             result_low[j] = numpy.mean([x[1] for x in low if x[0] == j])
    #         for j in names_high:
    #             result_precip[j] = numpy.mean([x[1] for x in precip if x[0] == j])
    #         all_names = set(list(names_high) + list(names_low) + list(names_precip))
    #         for name in all_names:
    #             result[name] = [result_high[name], result_low[name], result_precip[name]]
    #         return result



#     def count_missing_precipitation(self, list_of_days):
#         count = 0
#         for day in list_of_days:
#             if int(day.high) > MISSING and int(day.low) > MISSING and int(day.precip) == MISSING:
#                 count += 1
#         return count

#     def write_missing_precip(self, list_of_days, count):
#         answer = DESKTOP + 'answers/'
#         result = []
#         with open(os.path.join(answer, 'MissingPrcpData.out'), 'a') as f:
#             f.write(list_of_days[0].file_name + "\t" + str(count) + '\n')
#             result.append(str(count))
#         return result

#     def get_max_min_by_year(self, list_of_days):
#         years_high = defaultdict(list)
#         years_low = defaultdict(list)
#         for day in list_of_days:
#             if day.high > MISSING:
#                 years_high[day.date[:4]].append(float(day.high))
#             if day.low > MISSING:
#                 years_low[day.date[:4]].append(float(day.low))
#         return self.get_averages(years_high, years_low)

#     def get_averages(self, years_high, years_low):
#         high_avg = defaultdict(lambda: float(-9999))
#         low_avg = defaultdict(lambda: float(-9999))
#         for i in range(1985, 2015):
#             key = str(i)
#             if len(years_high[key]) > 0:
#                 high_avg[key] = sum(years_high[key])/len(years_high[key])
#             if len(years_low[key]) > 0:
#                 low_avg[key] = sum(years_low[key])/len(years_low[key])
#         return high_avg, low_avg

#     def get_total_precip(self, list_of_days):
#         total_precip = defaultdict(list)
#         final_precip = defaultdict(lambda: int(-9999))
#         for day in list_of_days:
#             total_precip[day.date[:4]].append(float(day.precip))
#         for i in range(1985, 2015):
#             key = str(i)
#             if total_precip[key]:
#                 final_precip[key] = sum(total_precip[key])/len(total_precip[key])
#         return final_precip

#     def write_answer_2(self, file_name, high_avg, low_avg, total_precip):
#         result = []
#         with open(os.path.join(DESKTOP + 'answers/', 'YearlyAverages.out'), 'a') as f:
#             for i in range(1985, 2015):
#                 key = str(i)
#                 string_data = '{}\t{}\t{:0.2f}\t{:0.2f}\t{:0.2f}'.format(
#                     file_name, key, high_avg[key], low_avg[key], total_precip[key])
#                 f.write(string_data + '\n')
#                 result.append(string_data.split('\t'))
#         return result

#     def count_all(self, years_list):
#         years_high = defaultdict(lambda: float(MISSING))
#         years_low = defaultdict(lambda: float(9999))
#         years_precip = defaultdict(lambda: float(MISSING))
#         count_high = defaultdict(int)
#         count_low = defaultdict(int)
#         count_precip = defaultdict(int)
#         for value in years_list:
#             if float(value[2]) > MISSING:
#                 years_high[value[1]] = max(float(value[2]), years_high[value[1]])
#             if float(value[3]) > MISSING:
#                 years_low[value[1]] = min(float(value[3]), years_low[value[1]])
#             if float(value[4]) > MISSING:
#                 years_precip[value[1]] = max(float(value[4]), years_precip[value[1]])
#         for value in years_list:
#             if years_high[value[1]] == float(value[2]) and float(value[2]) > MISSING:
#                 count_high[value[1]] += 1
#             if years_low[value[1]] == float(value[3]) and float(value[3]) > MISSING:
#                 count_low[value[1]] += 1
#             if years_precip[value[1]] == float(value[4]) and float(value[4]) > MISSING:
#                 count_precip[value[1]] += 1
#         return count_high, count_low, count_precip

#     def write_answer_3(self, years_high, years_low, years_precip):
#         result = []
#         with open(os.path.join(DESKTOP + 'answers', 'YearHistogram.out'), 'a') as f:
#             for i in range(1985, 2015):
#                 key = str(i)
#                 string_data = '{}\t{}\t{}\t{}'.format(
#                     key, years_high[key], years_low[key], years_precip[key]
#                         )
#                 f.write(string_data + '\n')
#                 result.append(string_data.split('\t'))
#         return result

#     def draw_histogram(self, counts):
#         with open(os.path.join(DESKTOP + 'answers/',  'YearHistogram_draw.txt'), 'a') as f:
#             for i in range(1985, 2015):
#                 key = str(i)
#                 bar = '{}'.format(key) + counts[key] * '#' + '\n'
#                 f.write(bar)

#     def calculate_pearson(self, weather, yields):
#         import math
#         years = len(weather)
#         weather_station_avg = (sum(weather)/len(weather))
#         yield_avg = (sum(yields)/len(yields))
#         diffprod = 0
#         weather_diff2 = 0
#         yield_diff2 = 0
#         for year in range(years):
#             weather_diff = weather[year] - weather_station_avg
#             yield_diff = yields[year] - yield_avg
#             diffprod += weather_diff * yield_diff
#             weather_diff2 += weather_diff * weather_diff
#             yield_diff2 += yield_diff * yield_diff
#         return diffprod / math.sqrt(weather_diff2 * yield_diff2)

#     def pearson(self, years_list, check):
#         data = {}
#         weather = defaultdict(float)
#         with open(os.path.join(DESKTOP + 'yld_data/' + 'US_corn_grain_yield.txt')) as f:
#             for line in f:
#                 new_list = line.strip().split('\t')
#                 data[new_list[0]] = float(new_list[1])
#         for file in years_list:
#             weather[file[1]] = float(file[check])
#         weather_list = [weather.get(x, 0) for x in weather.keys()]
#         yield_list = [data.get(x, 0) for x in data.keys()]
#         return self.calculate_pearson(weather_list, yield_list)

#     def write_answer_4(self, years_list):
#         result = []
#         with open(os.path.join(DESKTOP + 'answers/',  'Correlations.out'), 'a') as f:
#             for year in years_list:
#                 string_data = '{}\t{}\t{:0.2f}\t{:0.2f}\t'.format(
#                     year[0], self.pearson(years_list, 2), self.pearson(years_list, 3), self.pearson(years_list, 4)
#                 )
#                 result.append(string_data.strip('\t'))
#             for value in sorted(set(result)):
#                 f.write(value + '\n')

# if __name__ == "__main__":
#     path_wx_data = DESKTOP + 'wx_data/'
#     path_yld_data = DESKTOP + 'yld_data/'
#     try:
#         os.remove(DESKTOP + 'answers/' + 'YearlyAverages.out')
#         os.remove(DESKTOP + 'answers/' + 'MissingPrcpData.out')
#         os.remove(DESKTOP + 'answers/' + 'YearHistogram.out')
#         os.remove(DESKTOP + 'answers/' + 'YearHistogram_draw.txt')
#         os.remove(DESKTOP + 'answers/' + 'Correlations.out')
#     except:
#         pass
#     g = Weather()
#     for filename in os.listdir(path_wx_data):
#         data = []
#         new_data = []
#         years_list = []
#         with open(os.path.join(path_wx_data, filename)) as inputfile:
#             for line in inputfile:
#                 data.append(line.strip().split('\t'))
#             list_of_days = g.convert_to_days(filename, data)
#             count = g.count_missing_precipitation(list_of_days)
#             g.write_missing_precip(list_of_days, count)
#             high, low = g.get_max_min_by_year(list_of_days)
#             precip = g.get_total_precip(list_of_days)
#             years_list.extend(g.write_answer_2(filename, high, low, precip))
#             years_high, years_low, years_precip = g.count_all(years_list)
#             g.write_answer_4(years_list)
#     g.write_answer_3(years_high, years_low, years_precip)
