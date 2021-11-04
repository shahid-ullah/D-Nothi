# filename: src/clinic/views.py

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .data_loader import data_load


def top_x_illness(request):
    # plot1 data processing
    # data summary
    subjects = data_load()
    disease_set = list(set(subjects['症例']))
    month_set = list(set(subjects['month']))
    print(len(disease_set))
    print(len(month_set))

    # top 5 index
    import numpy as np

    counters_dis = np.array(
        [
            np.sum(subjects[subjects['症例'] == disease_set[a]]['症例別患者数'])
            for a in range(len(disease_set))
        ]
    )

    top_5_idx = counters_dis.argsort()[-5:]

    series_obj_p1 = []
    colors = ['#DA726E', '#E7DFAB', '#C5E7AB', '#ABE7D4', '#ABBEE7']
    count = 4
    for idx in top_5_idx:
        month_ws_data = []
        for mon in month_set:
            month_ws_data.append(
                int(
                    np.sum(
                        subjects[
                            (subjects['month'] == mon)
                            & (subjects['症例'] == disease_set[idx])
                        ]['症例別患者数']
                    )
                )
            )

        js_obj = {
            'name': disease_set[idx],
            'data': month_ws_data,
            'color': colors[count],
        }
        count -= 1
        series_obj_p1.append(js_obj)
    print(series_obj_p1)

    # complex automatic plot query

    year_set = sorted(list(set(subjects['year'])))
    print(year_set)

    dis_list = ['Light', 'Justice']  # disease_set

    dis_series_obj = {}

    print(dis_series_obj)
    print(dis_list)

    dum_list = ['aa', 'bb', 'cc']

    year_s = year_set[0]
    year_e = year_set[len(year_set) - 1]

    context = {
        'series_obj': json.dumps(series_obj_p1),
        'dis_series_obj': json.dumps(dis_series_obj),
        'dis_list': json.dumps(dis_list),
        'dum_list': json.dumps(dum_list),
        'year_s': json.dumps(year_s),
        'year_e': json.dumps(year_e),
    }

    return render(request, 'monthly_report/analyze_top_illness.html', context)
