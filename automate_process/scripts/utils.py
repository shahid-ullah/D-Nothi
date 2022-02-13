# automate_process/scripts/reports/utils.py
from datetime import datetime

from django.conf import settings


class utilsContainer:
    def __init__(self) -> None:
        self.MONTH_MAP_DICT = self.initialize_month_map()
        self.DAY_MAP_DICT = self.initialize_day_map()

    def load_dataframe(self, model, nrows=100):
        if settings.DEBUG:
            objs = model.objects.using('source_db').all()[:nrows]
        else:
            objs = model.objects.using('source_db').all()
        return objs

    def initialize_day_map(self):
        day_map_dict = {}
        for i in range(32):
            if i < 10:
                key1 = str(i)
                key2 = '0' + str(i)
                value = '0' + str(i)
                day_map_dict.setdefault(key1, value)
                day_map_dict.setdefault(key2, value)
            else:
                key = str(i)
                value = str(i)
                day_map_dict.setdefault(key, value)

        return day_map_dict

    def initialize_month_map(self):
        month_map_dict = {}
        for i in range(13):
            if i < 10:
                key1 = str(i)
                key2 = '0' + str(i)
                value = '0' + str(i)
                month_map_dict.setdefault(key1, value)
                month_map_dict.setdefault(key2, value)
            else:
                key = str(i)
                value = str(i)
                month_map_dict.setdefault(key, value)
        return month_map_dict

    def generate_year_month_day_key_and_report_date(self, year, month, day):
        year = str(year)
        month = str(month)
        day = str(day)

        month = self.MONTH_MAP_DICT[month]
        day = self.DAY_MAP_DICT[day]

        year_month_day = year + month + day
        report_date = year + "-" + month + "-" + day

        return year_month_day, report_date

    def generate_model_object_dictionary(self, request, year, month, day, count):
        year_month_day, report_date = self.generate_year_month_day_key_and_report_date(
            year, month, day
        )
        dict_ = {}
        dict_['year'] = year
        dict_['month'] = month
        dict_['day'] = day
        dict_['count_or_sum'] = count
        dict_['year_month_day'] = year_month_day
        dict_['report_date'] = report_date
        report_day = datetime(year, month, day)

        dict_['report_day'] = report_day

        try:
            if request.user.is_authenticated:
                dict_['creator'] = request.user
        except Exception as e:
            pass

        return dict_

    def format_and_load_to_mysql_db(self, request, groupby_date, model):
        last_report_date = ''

        for date, frame in groupby_date:
            last_report_date = date

            count = frame['id'].count()
            # print(f"date: {last_report_date}, count: {count}")

            dict_ = self.generate_model_object_dictionary(
                request, date.year, date.month, date.day, count
            )
            defaults = {'count_or_sum': count}

            try:
                obj = model.objects.get(year_month_day=dict_['year_month_day'])
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
            except model.DoesNotExist:
                obj = model(**dict_)
                obj.save()

        return last_report_date
