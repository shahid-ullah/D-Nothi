# filename: src/clinic/views.py

import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .data_loader import data_load_consultation


def analyze_consultation(request):
    # dynamic populate
    # data summary
    subjects = data_load_consultation()
    # subjects.head()

    consultancy_types = ['予防接種あり', '処方あり', '処置あり', '検査あり', '画像撮影あり', '文章あり']

    # con_cat_idx = []
    # for i in range(len(consultancy_set)):
    #     con_cat_idx.append([str(i + 1), consultancy_set[i]])
    #
    # consultancy_categories = con_cat_idx
    #
    # base_set = list(set(subjects['拠点名']))
    # base_cat_idx = []
    # for i in range(len(base_set)):
    #     base_cat_idx.append([str(i + 1), base_set[i]])
    #
    # base_categories = base_cat_idx

    context = {
        'consultancy_categories': consultancy_types,
    }

    return render(request, 'monthly_report/analyze_consultation.html', context)


@csrf_exempt
def analyze_consultation_detail(request):
    if request.method == 'POST':
        # recovert the data sending by the ajax post request
        consultation = request.POST['consultation']
        fromDate = request.POST['fromDate']
        toDate = request.POST['toDate']

        req_list = []  # requested illness_list

        for c in consultation:
            temp += c
            print(temp)
            if temp in consultation:
                print(temp + 'NABIL')
                req_list.append(temp)
                temp = ''

        print(req_list)

        # dynamic populate
        # data summary
        # subjects = data_load_consultation()

        consultations = ''

        for dis in req_list:
            if dis == req_list[len(req_list) - 1]:
                consultations += dis
            else:
                consultations += dis + ', '

        result = "Analysis for " + consultations

        # return the result to the ajax callback function
        return JsonResponse(
            json.dumps(
                {
                    'result': result,
                }
            ),
            safe=False,
        )

    return HttpResponse("From: analyze_consultation_details")
