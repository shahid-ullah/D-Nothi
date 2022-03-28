# SELECT count(DISTINCT(`employee_record_id`)) FROM `user_login_history` WHERE
# `created` >= '2022-01-01 00:00:00' AND `created` <= '2022-01-31 23:59:59'
from datetime import datetime

from dashboard_generate.models import ReportLoginTotalUsers


def get_single_digit_maps():
    map = {}
    for i in range(0, 10):
        value = f"0{i}"
        map.setdefault(i, value)

    return map


SINGLE_DIGIT_KEY_MAPS = get_single_digit_maps()


def generate_year_month_day_key_and_report_date(year, month, day):
    if month < 10:
        month = SINGLE_DIGIT_KEY_MAPS[month]

    if day < 10:
        day = SINGLE_DIGIT_KEY_MAPS[day]
    year_month_day = f"{year}{month}{day}"
    report_date = f"{year}-{month}-{day}"

    return year_month_day, report_date


def generate_model_object_dictionary(request, year, month, day, count):
    year_month_day, report_date = generate_year_month_day_key_and_report_date(
        year, month, day)
    model_object_dict = {
        'year': year,
        'month': month,
        'day': day,
        'count_or_sum': count,
        'year_month_day': year_month_day,
        'report_date': report_date,
        'report_day': datetime(year, month, day)
    }

    try:
        if request.user.is_authenticated:
            model_object_dict['creator'] = request.user
    except Exception as e:
        pass

    return model_object_dict


def format_and_load_to_mysql_db(request, groupby_date):
    last_report_date = ''

    for date, frame in groupby_date:
        last_report_date = date

        count = frame['employee_record_id'].nunique()
        employee_ids = {}

        for id in frame.employee_record_id.values:
            employee_ids.setdefault(int(id), 1)

        dict_ = generate_model_object_dictionary(request, date.year,
                                                 date.month, date.day, count)
        dict_['employee_record_ids'] = employee_ids

        defaults = {'count_or_sum': count, 'employee_record_ids': employee_ids}

        try:
            obj = ReportLoginTotalUsers.objects.get(
                year_month_day=dict_['year_month_day'])
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except ReportLoginTotalUsers.DoesNotExist:
            obj = ReportLoginTotalUsers(**dict_)
            obj.save()
    return last_report_date


def update(dataframe, request=None, *args, **kwargs):
    status = {}
    try:
        print()
        print('start processing login total users report')

        # values = objs.values('id', 'employee_record_id', 'created')

        # dataframe = pd.DataFrame(values)

        # remove null values
        # dataframe = dataframe.loc[dataframe.operation_date.notnull()]
        dataframe['created'] = dataframe.created.fillna(method='bfill')
        groupby_date = dataframe.groupby(dataframe.created.dt.date)

        last_report_date = format_and_load_to_mysql_db(request, groupby_date)
        print('End processing login total users report')
        print()
        status['last_report_date'] = str(last_report_date)
        status['status'] = 'success'
    except Exception as e:
        status['status'] = str(e)
        status['last_report_date'] = []

    return status
