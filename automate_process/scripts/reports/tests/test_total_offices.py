from datetime import datetime

import pytest

from dashboard_generate.models import ReportTotalOfficesModel

from .. import total_offices


def test_values_of_generate_object_map():
    report_date = datetime.now()
    number_of_offices = 500
    object_dic = total_offices.generate_object_map(report_date, number_of_offices)

    assert object_dic['year'] == report_date.year
    assert object_dic['month'] == report_date.month
    assert object_dic['day'] == report_date.day
    assert object_dic['report_date'] == str(report_date)
    assert object_dic['count_or_sum'] == int(number_of_offices)
    assert len(object_dic) == 5


def test_type_of_generate_object_map():
    report_date = datetime.now()
    number_of_offices = 500
    object_dic = total_offices.generate_object_map(report_date, number_of_offices)

    assert type(object_dic['year']) == int
    assert type(object_dic['month']) == int
    assert type(object_dic['day']) == int
    assert type(object_dic['report_date']) == str
    assert type(object_dic['count_or_sum']) == int


@pytest.mark.django_db
def test_object_creation():
    report_date = datetime.now()
    number_of_offices = 500
    object_dict = total_offices.generate_object_map(report_date, number_of_offices)
    count_or_sum = object_dict['count_or_sum']
    obj = ReportTotalOfficesModel.objects.create(**object_dict)
    assert obj.count_or_sum == count_or_sum
