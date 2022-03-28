# automate_process/scripts/nispottikritto_nothi.py
from datetime import datetime

from dashboard_generate.models import ReportNispottikrittoNothiModel


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
            obj = ReportNispottikrittoNothiModel.objects.get(
                year_month_day=dict_['year_month_day'])
            # obj = ReportTotalOfficesModel.objects.get(report_day=report_day)
            for key, value in defaults.items():
                setattr(obj, key, value)
            obj.save()
        except ReportNispottikrittoNothiModel.DoesNotExist:
            obj = ReportNispottikrittoNothiModel(**dict_)
            obj.save()
    return last_report_date


def update(dataframe, request=None, *args, **kwargs):
    status = {}
    try:
        print()
        print('start processing nispottikritto_nothi report')

        # values = objs.values('id', 'operation_date')
        # dataframe = pd.DataFrame(values)
        # dataframe = dataframe.loc[dataframe.operation_date.notnull()]
        dataframe['operation_date'] = dataframe.operation_date.fillna(
            method='bfill')
        groupby_date = dataframe.groupby(dataframe.operation_date.dt.date)

        last_report_date = format_and_load_to_mysql_db(request, groupby_date)
        print('End processing total_offices report')
        print()
        status['last_report_date'] = str(last_report_date)
        status['status'] = 'success'
    except Exception as e:
        status['status'] = str(e)
        status['last_report_date'] = []

    return status
