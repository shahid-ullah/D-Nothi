from datetime import datetime

from .. import login_total_users


def test_values_of_generate_model_object_dict():
    request = None
    report_date = datetime.now()
    count_or_sum = 580384
    office_id = 4598

    object_dict = login_total_users.generate_model_object_dict(request, report_date, count_or_sum, office_id)
    assert len(object_dict) == 8

    assert object_dict['year'] == report_date.year
    assert object_dict['month'] == report_date.month
    assert object_dict['day'] == report_date.day
    assert object_dict['year_month_day'] == str(report_date).replace('-', '')
    assert object_dict['report_date'] == str(report_date)
    assert object_dict['report_day'] == datetime(report_date.year, report_date.month, report_date.day)
    assert object_dict['count_or_sum'] == int(count_or_sum)
    assert object_dict['office_id'] == int(office_id)
