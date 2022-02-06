import json

from dashboard_generate.models import ReportTotalOfficesModel

FILENAME = ''
MODEL = ''

day_map_dict = {}
month_map_dict = {}

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

with open('user_login_history.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    mobile_app_users = data['mobile_app_users']
    i = 0
    for year_obj in mobile_app_users:
        year = year_obj['year']
        month_data = year_obj['month_data']

        for month_map in month_data:
            month = month_map['month']
            day_data = month_map['day_data']

            for day_map in day_data:
                i = i + 1
                day = day_map['day']
                count = day_map['count']

                # Generating key: year + month +day
                year = str(year)
                month = str(month)
                day = str(day)

                month = month_map_dict[month]
                day = day_map_dict[day]

                year_month_day = year + month + day

                year = int(year)
                month = int(month)
                day = int(day)
                count = int(count)

                try:
                    obj = report_mobile_app_users_model.objects.get(
                        year_month_day=year_month_day
                    )
                    # for key, value in defaults.items():
                    #     setattr(obj, key, value)
                    # obj.save()
                    print(i)
                except report_mobile_app_users_model.DoesNotExist:
                    print(i)
                    new_values = {
                        'year': year,
                        'month': month,
                        'day': day,
                        'count_or_sum': count,
                        'year_month_day': year_month_day,
                    }
                    obj = report_mobile_app_users_model(**new_values)
                    obj.save()
