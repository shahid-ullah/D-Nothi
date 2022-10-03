from datetime import datetime

from .. import login_total_users_not_distinct


def test_values_of_generate_model_object_dict():
    request = None
    office_id = 7988
    report_date = datetime.now()
    count_or_sum = 79998
    ministry_id = 56

    object_dict = login_total_users_not_distinct.generate_model_object_dict(
        request, office_id, report_date, count_or_sum, ministry_id
    )
    assert len(object_dict) == 7
    assert object_dict['year'] == report_date.year
    assert object_dict['month'] == report_date.month
    assert object_dict['day'] == report_date.day
    assert object_dict['report_date'] == datetime(report_date.year, report_date.month, report_date.day)
    assert object_dict['counts'] == int(count_or_sum)
    assert object_dict['office_id'] == int(office_id)
    assert object_dict['ministry_id'] == int(ministry_id)
