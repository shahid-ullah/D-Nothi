import json

import numpy as np
import pandas as pd
from django.shortcuts import render

from .models import ReportTotalOfficesModel


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def generate_year_map(objs):
    values = objs.values('year', 'month', 'day', 'count_or_sum')
    dataframe = pd.DataFrame(values)
    year_map = {}
    month_map = {}
    day_map = {}

    year_group_by = dataframe.groupby('year')
    for year, year_frame in year_group_by:
        year_map[year] = year_frame['count_or_sum'].sum()
        month_map[year] = {}
        day_map[year] = {}

        month_group_by = year_frame.groupby('month')

        for month, month_frame in month_group_by:
            month_map[year][month] = month_frame['count_or_sum'].sum()

            day_map[year][month] = {}

            day_group_by = month_frame.groupby('day')
            for day, day_frame in day_group_by:
                day_map[year][month][day] = day_frame['count_or_sum'].sum()

    return year_map, month_map, day_map
    # breakpoint()


# Create your views here.
def total_offices_view(request):
    objs = ReportTotalOfficesModel.objects.all()
    year_map, month_map, day_map = generate_year_map(objs)
    # breakpoint()

    # global offices_general_series, offices_'drilldown'_series
    # if offices_general_series and offices_'drilldown'_series:
    #     context = {
    #         'general_series': json.dumps(offices_general_series, cls=NpEncoder),
    #         ''drilldown'_series': json.dumps(offices_'drilldown'_series, cls=NpEncoder),
    #     }
    #     return render(request, 'monthly_report/dashboard.html', context)

    # general_series, 'drilldown'_series = load_total_offices_graph_data()

    # offices_general_series = copy.deepcopy(general_series)
    # offices_'drilldown'_series = copy.deepcopy('drilldown'_series)

    context = {
        'year_map': json.dumps(year_map, cls=NpEncoder),
        'month_map': json.dumps(month_map, cls=NpEncoder),
        'day_map': json.dumps(day_map, cls=NpEncoder),
    }

    return render(request, 'dashboard_generate/total_offices.html', context)
