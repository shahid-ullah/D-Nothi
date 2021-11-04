# filename: src/clinic/views.py

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .data_loader import data_load, data_load_with_age


def analyze_age_group(request):
    # dynamic populate
    # data summary
    # subjects.head()
    illness_set = ['All', '0-1', '2-5', '6-10', '11-14', '15-18']
    ill_cat_idx = []
    for i in range(len(illness_set)):
        ill_cat_idx.append([str(i + 1), illness_set[i]])

    illness_categories = ill_cat_idx
    ### MAPPING FROM AGE -> ILLNESS, MAIN VAR : AGE
    context = {'age_ranges': illness_categories, 'num_age': len(illness_set)}

    return render(request, 'monthly_report/analyze_age_group.html', context)


@csrf_exempt
def age_group_drilldown(request):
    if request.method == 'POST':

        subjects = data_load_with_age()

        # recovert the data sending by the ajax post request
        age_range = request.POST['illness']  # This is actually age range
        fromDate = request.POST['fromDate']  # This is start data
        toDate = request.POST['toDate']  # This is end data

        # fromAge = request.POST['fromAge']  # This is start data
        # toAge = request.POST['toAge']  # This is end data

        print(age_range)
        print(fromDate)
        print(toDate)
        # print(fromAge)
        # print(toAge)
        suffix = ''

        if fromDate != '':
            suffix = " from: " + fromDate + ' to: ' + toDate

        result = "Patients Visit by Age Group: " + age_range

        import time

        import numpy as np

        t_s = time.time()

        f_date_y = 0
        t_date_y = 1000000  # infinite, to get the full range

        if fromDate != '' and toDate != '':
            f_date_y = int(fromDate.split('-')[0])
            # print(f_date_y)
            t_date_y = int(toDate.split('-')[0])
            # print(t_date_y)

            f_date_m = int(fromDate.split('-')[1])
            # print(f_date_m)
            t_date_m = int(toDate.split('-')[1])
        # print(t_date_m)

        # only selecting year, if later needed will add month

        flag_all = False
        age_s = 1
        age_e = 1

        if age_range != 'All':
            age_s = int(age_range.split('-')[0])
            age_e = int(age_range.split('-')[1])

        # if fromAge != '':
        #     age_s = int(fromAge)
        # if toAge != '':
        #     age_e = int(toAge)

        if age_range == 'All':  # and (fromAge == '' and toAge == ''):
            flag_all = True

        print(age_s)
        print(age_e)

        # print(age_s)
        # print(age_e)

        # data primary
        age_name_drill = []
        age_wise = []

        # drilldown list of list

        drill_down_all = []
        drill_down_all_l2 = []
        bases = list(set(subjects['拠点名']))
        ills = list(set(subjects['症例']))
        # print(bases)

        # optimization start
        if flag_all:
            age_range_s = [0, 2, 6, 11, 15]
            age_range_e = [1, 5, 10, 14, 18]

            for a_i in range(len(age_range_s)):
                a_s = age_range_s[a_i]
                a_e = age_range_e[a_i]
                age_name_drill.append(str(a_s) + '-' + str(a_e))
                age_wise.append(
                    int(
                        len(
                            subjects[
                                (subjects['year'] >= f_date_y)
                                & (subjects['year'] <= t_date_y)
                                & (subjects['age'] >= a_s)
                                & (subjects['age'] <= a_e)
                            ]
                        )
                    )
                )
                bases = list(set(subjects['拠点名']))
                base_wise_age = []
                for base in bases:
                    cur_y = int(
                        len(
                            subjects[
                                (subjects['year'] >= f_date_y)
                                & (subjects['year'] <= t_date_y)
                                & (subjects['age'] >= a_s)
                                & (subjects['age'] <= a_e)
                                & (subjects['拠点名'] == base)
                            ]
                        )
                    )
                    base_wise_age.append([base, cur_y])
                drill_down_all.append(base_wise_age)

                ##### OPTIMIZATION BLOCK #####
                ill_wise_age_p = []
                t1 = time.time()
                for base in bases:
                    cur_y = list(
                        subjects[
                            (subjects['year'] >= f_date_y)
                            & (subjects['year'] <= t_date_y)
                            & (subjects['age'] >= a_s)
                            & (subjects['age'] <= a_e)
                            & (subjects['拠点名'] == base)
                        ]['症例']
                    )
                    ill_wise_age_p.append(cur_y)
                # 4.657801151275635
                t2 = time.time()
                print(t2 - t1)

                ill_wise_age = []
                b_i = 0
                for base in bases:
                    for ill in ills:
                        ill_wise_age.append([ill, ill_wise_age_p[b_i].count(ill)])
                    b_i += 1
                t2 = time.time()
                print(t2 - t1)

                ##### OPTIMIZATION BLOCK #####

                drill_down_all_l2.append(ill_wise_age)
        else:
            a_s = age_s
            a_e = age_e
            t1 = time.time()  # block start
            age_name_drill.append(str(a_s) + '-' + str(a_e))
            age_wise.append(
                int(
                    len(
                        subjects[
                            (subjects['year'] >= f_date_y)
                            & (subjects['year'] <= t_date_y)
                            & (subjects['age'] >= a_s)
                            & (subjects['age'] <= a_e)
                        ]
                    )
                )
            )
            # block 1 -> 0.007598

            t1 = time.time()

            base_wise_age = []
            for base in bases:
                cur_y = int(
                    len(
                        subjects[
                            (subjects['year'] >= f_date_y)
                            & (subjects['year'] <= t_date_y)
                            & (subjects['age'] >= a_s)
                            & (subjects['age'] <= a_e)
                            & (subjects['拠点名'] == base)
                        ]
                    )
                )
                base_wise_age.append([base, cur_y])
            drill_down_all.append(base_wise_age)
            # 0.04322

            t1 = time.time()

            # breakdown, optimization 1
            ###### OPTIMIZATION BLOCK ######
            ill_wise_age_p = []
            t1 = time.time()
            for base in bases:
                cur_y = list(
                    subjects[
                        (subjects['year'] >= f_date_y)
                        & (subjects['year'] <= t_date_y)
                        & (subjects['age'] >= a_s)
                        & (subjects['age'] <= a_e)
                        & (subjects['拠点名'] == base)
                    ]['症例']
                )
                ill_wise_age_p.append(cur_y)
            # 4.657801151275635
            t2 = time.time()
            print(t2 - t1)

            ill_wise_age = []
            b_i = 0
            for base in bases:
                for ill in ills:
                    ill_wise_age.append([ill, ill_wise_age_p[b_i].count(ill)])
                b_i += 1
            t2 = time.time()
            print(t2 - t1)

            ###### OPTIMIZATION BLOCK END ######

            drill_down_all_l2.append(ill_wise_age)
            # 4.657801151275635
            t2 = time.time()
            print(t2 - t1)

        t1 = time.time()
        print(age_name_drill)
        print(age_wise)
        print(drill_down_all)
        print(drill_down_all_l2)

        ser_primary_dict = {}
        ser_primary_dict['name'] = 'Age'
        ser_primary_dict['colorByPoint'] = 'true'
        ser_primary_dict['data'] = []

        ser_sec = []
        for i in range(len(age_name_drill)):
            ser_primary_dict['data'].append(
                {
                    'name': age_name_drill[i],
                    'y': age_wise[i],
                    'drilldown': age_name_drill[i],
                }
            )
            per_ager_data = {}
            per_ager_data['name'] = age_name_drill[i]
            per_ager_data['id'] = age_name_drill[i]
            # per_ager_data['drilldown'] = age_name_drill[i]
            per_ager_data['data'] = []
            for j in range(len(bases)):
                per_ager_data['data'].append(
                    {
                        'name': bases[j],
                        'y': drill_down_all[i][j][1],
                        'drilldown': bases[j],
                    }
                )

            ser_sec.append(per_ager_data)

            cnt = 0
            t1 = time.time()
            for j in range(len(bases)):
                per_baser_data = {}
                per_baser_data['name'] = bases[j]
                per_baser_data['id'] = bases[j]
                per_baser_data['data'] = []
                for k in range(len(ills)):
                    per_baser_data['data'].append(drill_down_all_l2[i][cnt])
                    cnt += 1
                ser_sec.append(per_baser_data)
            t2 = time.time()
            print(t2 - t1)
        ser_primary_dict = [ser_primary_dict]
        # print(ser_primary_dict)
        # print(ser_sec)
        t_e = time.time()
        print(t_e - t_s)

        # return the result to the ajax callback function
        return JsonResponse(
            json.dumps(
                {'result': result, 'pr_series': ser_primary_dict, 'sr_series': ser_sec}
            ),
            safe=False,
        )
