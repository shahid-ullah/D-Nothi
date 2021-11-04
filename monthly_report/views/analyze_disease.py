# filename: src/clinic/views.py

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .data_loader import data_load


def analyze_disease(request):
    # dynamic populate
    # data summary
    subjects = data_load()
    # subjects.head()
    illness_set = list(set(subjects['症例']))
    ill_cat_idx = []
    for i in range(len(illness_set)):
        ill_cat_idx.append([str(i + 1), illness_set[i]])

    illness_categories = ill_cat_idx

    context = {'illness_categories': illness_categories, 'num_dis': len(illness_set)}

    return render(request, 'monthly_report/analyze_disease.html', context)


@csrf_exempt
def analyze_disease_monthwise(request):
    if request.method == 'POST':
        # recovert the data sending by the ajax post request
        illness = request.POST['illness']
        fromDate = request.POST['fromDate']
        toDate = request.POST['toDate']

        print(illness)
        print(fromDate)
        print(toDate)

        import numpy as np

        f_date = int(fromDate.split('-')[0])
        print(f_date)
        t_date = int(toDate.split('-')[0])
        print(t_date)

        subjects = data_load()

        # year wise, 12 months sorted data
        data = []
        yr_ls = []
        yr_set = list(set(subjects['year']))
        for yr in yr_set:
            if yr >= f_date and yr <= t_date:
                yr_ls.append(yr)
        yr_ls = sorted(yr_ls)

        month_set = list(set(subjects['month']))
        bases = list(set(subjects['拠点名']))
        print(bases)

        data_by_base = []
        subjects.head()
        for yr in yr_ls:
            dict_temp = {}
            dict_temp['name'] = str(yr)
            base_dct = {}
            base_dct['name'] = str(yr)
            visit_ls = []
            base_ls = []
            for base in bases:
                k = int(
                    np.sum(
                        subjects[
                            (subjects['拠点名'] == base)
                            & (subjects['症例'] == illness)
                            & (subjects['year'] == yr)
                        ]['症例別患者数']
                    )
                )
                if k != 0:
                    base_ls.append(base)
            base_dct['data'] = list(set(base_ls))
            data_by_base.append(base_dct)
            for mon in month_set:
                visit_ls.append(
                    int(
                        np.sum(
                            subjects[
                                (subjects['month'] == mon)
                                & (subjects['症例'] == illness)
                                & (subjects['year'] == yr)
                            ]['症例別患者数']
                        )
                    )
                )
            dict_temp['data'] = visit_ls
            data.append(dict_temp)

        print(data_by_base)
        print(data)
        result = illness
        # return the result to the ajax callback function
        return JsonResponse(
            json.dumps(
                {'result': result, 'all_data': data, 'clinics_by_year': data_by_base}
            ),
            safe=False,
        )
