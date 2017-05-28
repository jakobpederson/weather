from collections import namedtuple, defaultdict
import os

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop/answers/")

Day = namedtuple('Day', ['file_name', 'date', 'high', 'low', 'precip'])
MISSING = -9999


class Weather():

    def convert_to_days(self, list_of_lists):
        result = []
        for value in list_of_lists:
            result.append(Day(file_name=value[0], date=value[1], high=value[2], low=value[3], precip=value[4]))
        return result

    def count_missing_precipitation(self, list_of_lists):
        count = 0
        list_of_days = self.convert_to_days(list_of_lists)
        for day in list_of_days:
            if day.high > MISSING and day.low > MISSING and day.precip == MISSING:
                count += 1
        return count

    def write_missing_precip(self, list_of_days, count):
        try:
            with open(os.path.join(DESKTOP, 'MissingPrcpData.out'), 'a') as f:
                f.write(list_of_days[0].file_name + "\t" + str(count) + '\n')
        except:
            with open(os.path.join(DESKTOP, 'MissingPrcpData.out'), 'w') as f:
                f.write(list_of_days[0].file_name + "\t" + str(count) + '\n')

    def get_max_min_by_year(self, list_of_days):
        years_high = defaultdict(float)
        years_low = defaultdict(float)
        for day in list_of_days:
            years_high[day.date[:4]] = max(day.high, years_high[day.date[:4]])
            if years_low[day.date[:4]]:
                years_low[day.date[:4]] = min(day.low, years_low[day.date[:4]])
            else:
                years_low[day.date[:4]] = day.low
        return {'high': years_high, 'low': years_low}
