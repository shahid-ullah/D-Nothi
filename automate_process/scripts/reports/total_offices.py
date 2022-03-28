# SELECT count(id) FROM offices WHERE date(created) <= '2020-09-30' AND active_status =1;
# Caution: Datafame is not processed according to this query
# This is not cumulative count
from datetime import datetime

from dashboard_generate.models import ReportTotalOfficesModel


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

        count = frame['id'].count()

        dict_ = generate_model_object_dictionary(request, date.year,
                                                 date.month, date.day, count)
        defaults = {'count_or_sum': count}

        try:
            object = ReportTotalOfficesModel.objects.get(
                year_month_day=dict_['year_month_day'])
            for key, value in defaults.items():
                setattr(object, key, value)
            object.save()
        except ReportTotalOfficesModel.DoesNotExist:
            object = ReportTotalOfficesModel(**dict_)
            object.save()
    return last_report_date


def update(dataframe, request=None, *args, **kwargs):
    status = {}
    try:
        print()
        print('start processing total_offices report')
        dataframe = dataframe.copy(deep=True)

        # values = objs.values('id', 'active_status', 'created')

        # dataframe = pd.DataFrame(values)
        dataframe = dataframe[dataframe.active_status == 1]
        # dataframe = dataframe.loc[dataframe.created.notnull()]
        dataframe['created'] = dataframe.created.fillna(method='bfill')
        groupby_date = dataframe.groupby(dataframe.created.dt.date)

        last_report_date = format_and_load_to_mysql_db(request, groupby_date)
        print('End processing total_offices report')
        print()
        status['last_report_date'] = str(last_report_date)
        status['status'] = 'success'
    except Exception as e:
        status['status'] = str(e)
        status['last_report_date'] = ''

    return status
