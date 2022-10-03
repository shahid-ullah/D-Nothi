from datetime import datetime

from .. import android_ios_users


def test_values_of_generate_model_object_dict():
    request = None
    report_date = datetime.now()
    count_or_sum = 3000
    office_id = 8002

    object_dic = android_ios_users.generate_model_object_dict(request, report_date, count_or_sum, office_id)
    assert len(object_dic) == 8
    assert object_dic['year'] == report_date.year
    assert object_dic['month'] == report_date.month
    assert object_dic['day'] == report_date.day
    assert object_dic['year_month_day'] == str(report_date).replace('-', '')
    assert object_dic['report_date'] == str(report_date)
    assert object_dic['report_day'] == datetime(report_date.year, report_date.month, report_date.day)
    assert object_dic['count_or_sum'] == int(count_or_sum)
    assert object_dic['office_id'] == int(office_id)
