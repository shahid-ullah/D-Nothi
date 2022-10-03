from datetime import datetime

from .. import upokarvogi


def test_values_of_generate_model_object_dict():
    request = None
    report_date = datetime.now()
    upokarvogi_sum = 8080808
    office_id = 57

    object_dict = upokarvogi.generate_model_object_dict(request, report_date, upokarvogi_sum, office_id)

    assert len(object_dict) == 8
    assert object_dict['year'] == report_date.year
    assert object_dict['month'] == report_date.month
    assert object_dict['day'] == report_date.day
    assert object_dict['year_month_day'] == str(report_date).replace('-', '')
    assert object_dict['report_date'] == str(report_date)
    assert object_dict['report_day'] == datetime(report_date.year, report_date.month, report_date.day)
    assert object_dict['count_or_sum'] == int(upokarvogi_sum)
    assert object_dict['office_id'] == int(office_id)
