# filename: src/clinic/views.py

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .data_loader import data_load

months_list = [
    '',
    ' 1月',
    ' 2月',
    ' 3月',
    ' 4月',
    ' 5月',
    ' 6月',
    ' 7月',
    ' 8月',
    ' 9月',
    '10月',
    '11月',
    '12月',
]


def predict_monthly_visit(request):
    # dynamic populate
    # data summary
    print('TIME SERIES AGGREGATED')
    subjects = data_load()
    # subjects.head()
    illness_set = list(set(subjects['症例']))
    ill_cat_idx = [['0', 'All']]
    for i in range(len(illness_set)):
        ill_cat_idx.append([str(i + 1), illness_set[i]])

    illness_categories = ill_cat_idx

    context = {
        'illness_categories': illness_categories,
        'num_dis': len(illness_set),
        'num_mon': 12,
        'months': months_list[1:],
    }

    return render(request, 'monthly_report/predict_monthly_visit.html', context)


@csrf_exempt
def predict_monthly_visitor_count(request):
    subjects = data_load()
    print('Entered')
    if request.method == 'POST':
        # select disease
        c_dis = request.POST['illness']
        c_mon = int(request.POST['mon'][:-1])
        print(c_dis)
        print(c_mon)
        import numpy as np

        subjects = subjects.sort_values(['year', 'month'])

        c_dis = c_dis[: -len(c_mon)]
        print(c_dis)

        ills = list(set(subjects['症例']))
        print(ills)
        final_list = []
        years_all = sorted(list(set(subjects['year'])))
        years = years_all[: len(years_all) - 1]
        print(years)
        months = list(set(subjects['month']))
        print(months)

        data_root = {}

        # data_root['headers'] = []

        c_mon = int(c_mon)

        b_mon = c_mon - 1
        a_mon = c_mon + 1
        yr_hd = ['症例']
        # linear model

        for yr in years:

            if c_mon == 1:
                if yr == years[0]:
                    yr_hd.append('No data')
                    yr_hd.append(str(c_mon) + ', ' + str(yr))
                    yr_hd.append(str(c_mon + 1) + ', ' + str(yr))
                else:
                    yr_hd.append(str(12) + ', ' + str(yr - 1))
                    yr_hd.append(str(c_mon) + ', ' + str(yr))
                    yr_hd.append(str(c_mon + 1) + ', ' + str(yr))
            elif c_mon == 12:
                if yr == years[len(years) - 1]:
                    yr_hd.append(str(c_mon - 1) + ', ' + str(yr))
                    yr_hd.append(str(c_mon) + ', ' + str(yr))
                    yr_hd.append('No data')
                else:
                    yr_hd.append(str(c_mon - 1) + ', ' + str(yr))
                    yr_hd.append(str(c_mon) + ', ' + str(yr))
                    yr_hd.append(str(1) + ', ' + str(yr + 1))
            else:
                yr_hd.append(str(c_mon - 1) + ', ' + str(yr))
                yr_hd.append(str(c_mon) + ', ' + str(yr))
                yr_hd.append(str(c_mon + 1) + ', ' + str(yr))

        yr_hd.append(
            'Prediction for ' + str(c_mon) + ', ' + str(years_all[len(years_all) - 1])
        )
        yr_hd.append(
            'Actual Data for ' + str(c_mon) + ', ' + str(years_all[len(years_all) - 1])
        )
        data_root['0'] = yr_hd

        # final_list.append(headers)

        if c_dis != 'All':
            c_mon = int(c_mon)

            data = {}
            for mn in months:
                for yr in years_all:
                    data[mn, yr] = 0

            for mn in months:
                for yr in years_all:
                    data[mn, yr] += int(
                        np.sum(
                            subjects[
                                (subjects['month'] == mn)
                                & (subjects['year'] == yr)
                                & (subjects['症例'] == c_dis)
                            ]['症例別患者数']
                        )
                    )

            # c_dis = '1' # TEMPORARY

            yr_hd = [c_dis]
            for yr in years:
                if c_mon == 1:
                    if yr == years[0]:
                        yr_hd.append(0)
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[c_mon + 1, yr])
                    else:
                        yr_hd.append(data[12, yr - 1])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[c_mon + 1, yr])
                elif c_mon == 12:
                    if yr == years[len(years) - 1]:
                        yr_hd.append(data[c_mon - 1, yr])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(0)
                    else:
                        yr_hd.append(data[c_mon - 1, yr])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[1, yr + 1])
                else:
                    yr_hd.append(data[c_mon - 1, yr])
                    yr_hd.append(data[c_mon, yr])
                    yr_hd.append(data[c_mon + 1, yr])

            prev_data = yr_hd[1:]
            # print('PREV', prev_data)
            param_weight = [0.85 if x % 3 == 1 else 0.35 for x in range(len(prev_data))]

            import math

            sc_factor = 5
            slow_expo = [
                math.exp(i / sc_factor) / math.exp((len(prev_data) - 1) / sc_factor)
                for i in range(len(prev_data))
            ]
            seq_model = np.multiply(slow_expo, param_weight)
            pred = np.sum(np.multiply(seq_model, prev_data)) / (np.sum(seq_model))
            yr_hd.append(int(pred))
            yr_hd.append(data[c_mon, years_all[len(years_all) - 1]])
            data_root['1'] = yr_hd

        else:

            idx = 1
            # Pre-processing to pre-calculate the disease list separately
            # Pandas queries are slow, O(n), needed to remove a single boolean
            # compare query
            a_ls = {}
            a_ls_data = {}
            for mn in months:
                for yr in years_all:
                    a_ls[mn, yr] = list(
                        subjects[(subjects['month'] == mn) & (subjects['year'] == yr)][
                            '症例'
                        ]
                    )
                    a_ls_data[mn, yr] = list(
                        subjects[(subjects['month'] == mn) & (subjects['year'] == yr)][
                            '症例別患者数'
                        ]
                    )
            data = {}
            for mn in months:
                for yr in years_all:
                    data[mn, yr] = 0

            for c_dis in ills:
                c_mon = int(c_mon)

                for mn in months:
                    for yr in years_all:
                        c_idx = [
                            i for i, val in enumerate(a_ls[mn, yr]) if val == c_dis
                        ]
                        # get all the indices with a specific country
                        data[mn, yr] = int(sum([a_ls_data[mn, yr][i] for i in c_idx]))

                # c_dis = '1' # TEMPORARY

                yr_hd = [c_dis]
                for yr in years:
                    if c_mon == 1:
                        if yr == years[0]:
                            yr_hd.append(0)
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(data[c_mon + 1, yr])
                        else:
                            yr_hd.append(data[12, yr - 1])
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(data[c_mon + 1, yr])
                    elif c_mon == 12:
                        if yr == years[len(years) - 1]:
                            yr_hd.append(data[c_mon - 1, yr])
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(0)
                        else:
                            yr_hd.append(data[c_mon - 1, yr])
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(data[1, yr + 1])
                    else:
                        yr_hd.append(data[c_mon - 1, yr])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[c_mon + 1, yr])
                prev_data = yr_hd[1:]
                # print('PREV', prev_data)
                import math

                sc_factor = 5
                param_weight = [
                    0.85 if x % 3 == 1 else 0.35 for x in range(len(prev_data))
                ]

                slow_expo = [
                    math.exp(i / sc_factor) / math.exp((len(prev_data) - 1) / sc_factor)
                    for i in range(len(prev_data))
                ]
                seq_model = np.multiply(slow_expo, param_weight)
                pred = np.sum(np.multiply(seq_model, prev_data)) / (np.sum(seq_model))
                yr_hd.append(int(pred))
                yr_hd.append(data[c_mon, years_all[len(years_all) - 1]])
                data_root[str(idx)] = yr_hd
                idx += 1

        print(data_root)
        # print(data)
        print("DONE--")
        analytics_summary = 'The time series shows some form of causality.'

        # return the result to the ajax callback function
        return JsonResponse(
            json.dumps(
                {
                    'result': analytics_summary,
                    'res_pred': final_list,
                    'data_root': data_root,
                }
            ),
            safe=False,
        )


@csrf_exempt
def generate_view(request):

    subjects = data_load()

    if request.method == 'POST':
        # select disease
        c_dis = request.POST['illness']
        c_mon = request.POST['month']

        import numpy as np

        subjects = subjects.sort_values(['year', 'month'])

        c_dis = c_dis[: -len(c_mon)]

        ills = list(set(subjects['症例']))
        years_all = sorted(list(set(subjects['year'])))
        years = years_all[: len(years_all) - 1]
        months = list(set(subjects['month']))

        data_root = {}

        c_mon = int(c_mon[:-1])
        yr_hd = ['症例']

        for yr in years:
            if c_mon == 1:
                yr_hd.append(str(months_list[12]) + ', ' + str(yr - 1))
                yr_hd.append(str(months_list[c_mon]) + ', ' + str(yr))
                yr_hd.append(str(months_list[c_mon + 1]) + ', ' + str(yr))
            elif c_mon == 12:
                yr_hd.append(str(months_list[c_mon - 1]) + ', ' + str(yr))
                yr_hd.append(str(months_list[c_mon]) + ', ' + str(yr))
                yr_hd.append(str(months_list[1]) + ', ' + str(yr + 1))
            else:
                yr_hd.append(str(months_list[c_mon - 1]) + ', ' + str(yr))
                yr_hd.append(str(months_list[c_mon]) + ', ' + str(yr))
                yr_hd.append(str(months_list[c_mon + 1]) + ', ' + str(yr))

        yr_hd.append(
            'Prediction for '
            + str(months_list[c_mon])
            + ', '
            + str(years_all[len(years_all) - 1])
        )
        yr_hd.append(
            'Actual Data for '
            + str(months_list[c_mon])
            + ', '
            + str(years_all[len(years_all) - 1])
        )
        data_root['0'] = yr_hd

        # final_list.append(headers)

        if c_dis != 'All':
            c_mon = int(c_mon)

            data = {}
            for mn in months:
                for yr in years_all:
                    data[mn, yr] = 0

            for mn in months:
                for yr in years_all:
                    data[mn, yr] += int(
                        np.sum(
                            subjects[
                                (subjects['month'] == mn)
                                & (subjects['year'] == yr)
                                & (subjects['症例'] == c_dis)
                            ]['症例別患者数']
                        )
                    )

            # c_dis = '1' # TEMPORARY

            yr_hd = [c_dis]
            for yr in years:
                if c_mon == 1:
                    if yr == years[0]:
                        yr_hd.append(0)
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[c_mon + 1, yr])
                    else:
                        yr_hd.append(data[12, yr - 1])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[c_mon + 1, yr])
                elif c_mon == 12:
                    if yr == years[len(years) - 1]:
                        yr_hd.append(data[c_mon - 1, yr])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(0)
                    else:
                        yr_hd.append(data[c_mon - 1, yr])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[1, yr + 1])
                else:
                    yr_hd.append(data[c_mon - 1, yr])
                    yr_hd.append(data[c_mon, yr])
                    yr_hd.append(data[c_mon + 1, yr])

            prev_data = yr_hd[1:]
            # print('PREV', prev_data)
            param_weight = [0.85 if x % 3 == 1 else 0.35 for x in range(len(prev_data))]

            import math

            sc_factor = 5
            slow_expo = [
                math.exp(i / sc_factor) / math.exp((len(prev_data) - 1) / sc_factor)
                for i in range(len(prev_data))
            ]
            seq_model = np.multiply(slow_expo, param_weight)
            pred = np.sum(np.multiply(seq_model, prev_data)) / (np.sum(seq_model))
            yr_hd.append(int(pred))
            yr_hd.append(data[c_mon, years_all[len(years_all) - 1]])
            data_root['1'] = yr_hd

        else:

            idx = 1
            # Pre-processing to pre-calculate the disease list separately
            # Pandas queries are slow, O(n), needed to remove a single boolean
            # compare query
            a_ls = {}
            a_ls_data = {}
            for mn in months:
                for yr in years_all:
                    a_ls[mn, yr] = list(
                        subjects[(subjects['month'] == mn) & (subjects['year'] == yr)][
                            '症例'
                        ]
                    )
                    a_ls_data[mn, yr] = list(
                        subjects[(subjects['month'] == mn) & (subjects['year'] == yr)][
                            '症例別患者数'
                        ]
                    )
            data = {}
            for mn in months:
                for yr in years_all:
                    data[mn, yr] = 0

            for c_dis in ills:
                c_mon = int(c_mon)

                for mn in months:
                    for yr in years_all:
                        c_idx = [
                            i for i, val in enumerate(a_ls[mn, yr]) if val == c_dis
                        ]
                        # get all the indices with a specific country
                        data[mn, yr] = int(sum([a_ls_data[mn, yr][i] for i in c_idx]))

                # c_dis = '1' # TEMPORARY

                yr_hd = [c_dis]
                for yr in years:
                    if c_mon == 1:
                        if yr == years[0]:
                            yr_hd.append(0)
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(data[c_mon + 1, yr])
                        else:
                            yr_hd.append(data[12, yr - 1])
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(data[c_mon + 1, yr])
                    elif c_mon == 12:
                        if yr == years[len(years) - 1]:
                            yr_hd.append(data[c_mon - 1, yr])
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(0)
                        else:
                            yr_hd.append(data[c_mon - 1, yr])
                            yr_hd.append(data[c_mon, yr])
                            yr_hd.append(data[1, yr + 1])
                    else:
                        yr_hd.append(data[c_mon - 1, yr])
                        yr_hd.append(data[c_mon, yr])
                        yr_hd.append(data[c_mon + 1, yr])
                prev_data = yr_hd[1:]
                # print('PREV', prev_data)
                import math

                sc_factor = 5
                param_weight = [
                    0.85 if x % 3 == 1 else 0.35 for x in range(len(prev_data))
                ]

                slow_expo = [
                    math.exp(i / sc_factor) / math.exp((len(prev_data) - 1) / sc_factor)
                    for i in range(len(prev_data))
                ]
                seq_model = np.multiply(slow_expo, param_weight)
                pred = np.sum(np.multiply(seq_model, prev_data)) / (np.sum(seq_model))
                yr_hd.append(int(pred))
                yr_hd.append(data[c_mon, years_all[len(years_all) - 1]])
                data_root[str(idx)] = yr_hd
                idx += 1

        analytics_summary = 'Patient Visit Prediction for the month'
        print(data_root)

        context = {
            'result': analytics_summary,
            'analyzed_data': data_root,
            'idx': ['1', '2', '3'],
        }
        return render(
            request, 'monthly_report/predict_monthly_visit_data.html', context
        )
