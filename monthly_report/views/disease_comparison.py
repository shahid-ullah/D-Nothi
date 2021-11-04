# filename: src/clinic/views.py

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .data_loader import data_load


def compare_diseases(request):
    # dynamic populate
    # data summary
    subjects = data_load()
    # subjects.head()
    illness_set = list(set(subjects['症例']))
    ill_cat_idx = []
    for i in range(len(illness_set)):
        ill_cat_idx.append([str(i + 1), illness_set[i]])

    illness_categories = ill_cat_idx

    # pre-rewuisite for table populate
    subjects = subjects.sort_values(['year', 'month'])

    yr_ls = []
    yr_set = list(set(subjects['year']))
    yr_ls = sorted(yr_set)
    month_set = list(set(subjects['month']))

    timeline = []
    month_map = [
        '',
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
    ]
    for yr in yr_ls:
        for mn in month_set:
            timeline.append(month_map[mn] + ', ' + str(yr))
    print(timeline)

    mon_y_list = []
    for i in range(len(timeline)):
        mon_y_list.append([str(i + 1), timeline[i]])
    print(mon_y_list)

    context = {
        'illness_categories': illness_categories,
        'num_dis': len(illness_set),
        'mon_y_list': mon_y_list,
        'num_timeline': len(mon_y_list),
    }

    return render(request, 'monthly_report/compare_disease.html', context)


@csrf_exempt
def compare_diseases_monthwise(request):
    if request.method == 'POST':
        # recovert the data sending by the ajax post request
        illness = request.POST['illness']

        # dynamic populate
        # data summary
        subjects = data_load()
        # subjects.head()
        illness_set = list(set(subjects['症例']))

        temp = ''

        req_list = []  # requested illness_list

        for c in illness:
            temp += c
            print(temp)
            if temp in illness_set:
                print(temp + 'NABIL')
                req_list.append(temp)
                temp = ''

        print(req_list)

        fromDate = request.POST['fromDate']
        toDate = request.POST['toDate']

        multi_illness = request.POST['multi_illness']

        print(multi_illness)

        print(illness)
        print(fromDate)
        print(toDate)

        # to django script
        # start from here copy

        subjects = subjects.sort_values(['year', 'month'])

        multi_illness = req_list

        print(multi_illness)

        print(fromDate)
        print(toDate)

        import numpy as np

        f_date_y = int(fromDate.split('-')[0])
        print(f_date_y)
        t_date_y = int(toDate.split('-')[0])
        print(t_date_y)

        f_date_m = int(fromDate.split('-')[1])
        print(f_date_m)
        t_date_m = int(toDate.split('-')[1])
        print(t_date_m)

        series_multi_illness = []

        yr_ls = []
        yr_set = list(set(subjects['year']))
        for yr in yr_set:
            if yr >= f_date_y and yr <= t_date_y:
                yr_ls.append(yr)

        yr_ls = sorted(yr_ls)
        # month_set = list(set(subjects['month']))

        timeline_m = []  # parallel
        timeline_y = []

        print(yr_ls)

        # special case: bug, if just 1 month
        for yr in yr_ls:
            if yr == yr_ls[0]:
                for mn in range(f_date_m, 13):
                    timeline_m.append(mn)
                    timeline_y.append(yr)
            elif yr == yr_ls[len(yr_ls) - 1]:
                for mn in range(1, t_date_m + 1):
                    timeline_m.append(mn)
                    timeline_y.append(yr)
            else:
                for mn in range(1, 13):
                    timeline_m.append(mn)
                    timeline_y.append(yr)

        print(timeline_m)
        print(timeline_y)

        series_multi_illness = []

        # colors for each separate line plot
        colors = [
            '#ff5733',
            ' #c33030',
            ' #e2a358',
            ' #e2dc58',
            ' #e2b258',
            ' #c7e258',
            ' #e25893',
            ' #e25871',
            ' #e258c7',
        ]

        count = 0
        for c_dis in multi_illness:

            dis_dict = {}
            dis_dict['name'] = c_dis

            visit_ls = []
            for mny_i in range(len(timeline_m)):
                visit_ls.append(
                    int(
                        np.sum(
                            subjects[
                                (subjects['month'] == timeline_m[mny_i])
                                & (subjects['症例'] == c_dis)
                                & (subjects['year'] == timeline_y[mny_i])
                            ]['症例別患者数']
                        )
                    )
                )
            dis_dict['data'] = visit_ls
            if count == len(multi_illness):
                count = 0
            dis_dict['color'] = colors[count]
            count += 1
            print(dis_dict)
            series_multi_illness.append(dis_dict)

        print(series_multi_illness)

        cat_tim_m_jp = [str(a) + '月' for a in timeline_m]
        print(cat_tim_m_jp)

        from random import randint

        plot_bands = []

        st = 0
        # en = 0
        last_y = timeline_y[0]
        for i in range(len(timeline_y)):
            if (timeline_y[i] != last_y) or (i == len(timeline_y) - 1):
                dict_pb = {}
                dict_pb['from'] = st - 0.5
                dict_pb['to'] = i - 0.5
                if i == len(timeline_y) - 1:
                    dict_pb['to'] = i + 0.5
                dict_pb['color'] = 'rgba(%d, %d, %d, 0.18)' % (
                    randint(0, 255),
                    randint(0, 255),
                    randint(0, 255),
                )
                dict_pb['label'] = {'text': last_y, 'align': 'center'}
                plot_bands.append(dict_pb)
                last_y = timeline_y[i]
                st = i

        print(plot_bands)

        illness = ''

        for dis in req_list:
            if dis == req_list[len(req_list) - 1]:
                illness += dis
            else:
                illness += dis + ', '

        result = "Patient visit for " + illness

        # return the result to the ajax callback function
        return JsonResponse(
            json.dumps(
                {
                    'result': result,
                    'plot_bands': plot_bands,
                    'cat_tim_m_jp': cat_tim_m_jp,
                    'series_multi_illness': series_multi_illness,
                }
            ),
            safe=False,
        )


@csrf_exempt
def analyze_illness_gen_table(request):
    return JsonResponse(json.dumps({'datam': ''}), safe=False)
