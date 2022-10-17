import datetime

import pytest
from django.urls import reverse

from dashboard_generate.models import ReportNispottikrittoNothiModel

# @pytest.fixture(scope='module')


@pytest.mark.django_db(databases=['default', 'source_db', 'backup_source_db'])
def test_nispottikritto_nothi_view(client):
    dic = {
        'year_month_day': '20160210',
        'creator_id': None,
        'year': 2016,
        'month': 2,
        'day': 10,
        'count_or_sum': 1,
        'office_id': None,
        'created': datetime.datetime(2022, 9, 12, 16, 7, 2, 576654),
        'updated': datetime.datetime(2022, 9, 12, 16, 7, 2, 576680),
        'report_date': '2016-02-10',
        'report_day': datetime.datetime(2016, 2, 10, 0, 0),
    }
    ReportNispottikrittoNothiModel.objects.create(**dic)
    url = reverse('nispottikritto_nothi')
    response = client.get(url)
    assert response.status_code == 200
