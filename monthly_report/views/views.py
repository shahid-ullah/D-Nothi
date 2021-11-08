# filename: src/clinic/views.py

import json

import numpy as np
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..apps import MonthlyReportConfig
from ..utils import load_nisponno_records_table, load_office_table
from .data_loader import data_load, data_load_dashboard


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def analyze(request):
    # plot1 data processing
    # data summary
    # subjects = data_load()
    # disease_set = list(set(subjects['症例']))
    # month_set = list(set(subjects['month']))
    # print(len(disease_set))
    # print(len(month_set))
    #
    # # top 5 index
    # import numpy as np
    # counters_dis = np.array(
    #     [np.sum(subjects[subjects['症例'] == disease_set[a]]['症例別患者数']) for a in range(len(disease_set))])
    #
    # top_5_idx = counters_dis.argsort()[-5:]
    #
    # series_obj_p1 = []
    # colors = ['#DA726E', '#E7DFAB', '#C5E7AB', '#ABE7D4', '#ABBEE7']
    # count = 4
    # for idx in top_5_idx:
    #     month_ws_data = []
    #     for mon in month_set:
    #         month_ws_data.append(
    #             int(np.sum(subjects[(subjects['month'] == mon) & (subjects['症例'] == disease_set[idx])]['症例別患者数'])))
    #
    #     js_obj = {
    #         'name': disease_set[idx],
    #         'data': month_ws_data,
    #         'color': colors[count]
    #     }
    #     count -= 1
    #     series_obj_p1.append(js_obj)
    # print(series_obj_p1)
    #
    # # complex automatic plot query
    #
    # year_set = sorted(list(set(subjects['year'])))
    # print(year_set)
    #
    # dis_list = ['Light', 'Justice']  # disease_set
    #
    # dis_series_obj = {}
    #
    # print(dis_series_obj)
    # print(dis_list)
    #
    # dum_list = ['aa', 'bb', 'cc']
    #
    # year_s = year_set[0]
    # year_e = year_set[len(year_set) - 1]

    series_obj_p1, dis_series_obj, dis_list, year_s, year_e = top_illness()

    subjects = data_load_dashboard()
    subjects = subjects.sort_values(by='start_date')

    # pre-process/modify dataframe
    a_tim = subjects['診察時間（分）']

    # converting timestamp to minute range
    a_tot_tim = timelist(a_tim)
    subjects['time'] = a_tot_tim

    year_col = [d[:4] for d in subjects['start_date']]
    year_mon = [d[5:7] for d in subjects['start_date']]

    subjects['year_col'] = year_col
    subjects['year_mon'] = year_mon

    analyze_waiting_time(subjects)
    analyze_patients_count(subjects)
    analyze_department_visit(subjects)
    analyze_department_visit_monthly(subjects)
    analyze_monthly_patients_visit_by_clinic(subjects)
    analyze_staff_count_by_clinic(subjects)
    analyze_waiting_time_by_clinic(subjects)
    analyze_doctor_patients_count(subjects)

    context = {
        'series_obj': json.dumps(series_obj_p1),
        'dis_series_obj': json.dumps(dis_series_obj),
        'dis_list': json.dumps(dis_list),
        'year_s': json.dumps(year_s),
        'year_e': json.dumps(year_e),
        'waiting_time': waiting_time_json,
        'waiting_time_by_clinic': json.dumps(waiting_time_by_clinic),
        'patients': json.dumps(patients),
        'department_visits': json.dumps(department_visits),
        'department_visits_monthly': json.dumps(department_visits_monthly),
        'monthly_patient_visit_count': json.dumps(monthly_patient_visit_count),
        'staff_count_by_clinic': json.dumps(staff_count),
        'doctor_patients_count': json.dumps(doctor_patients_count),
    }

    return render(request, 'monthly_report/analyze.html', context)


def dashboard(request):
    load_office_table()

    # offices_df = MonthlyReportConfig.offices_df
    offices_df = settings.OFFICES_CSV_FILE_PATH
    # years = offices_df.year.values
    # breakpoint()
    # print(list(set(years)))
    # years = list(set(years))
    office_count = offices_df.groupby('year').size()
    # type(office_count)
    office_numbers = list(office_count.values)
    # office_count.index
    # type(office_count.index)
    # dir(office_count.index)
    # office_count.index.array
    office_years = list(office_count.index.values)
    # breakpoint()

    # series_obj_p1, dis_series_obj, dis_list, year_s, year_e = top_illness()

    # subjects = data_load_dashboard()
    # subjects = subjects.sort_values(by='start_date')

    # # pre-process/modify dataframe
    # a_tim = subjects['診察時間（分）']

    # # converting timestamp to minute range
    # a_tot_tim = timelist(a_tim)
    # subjects['time'] = a_tot_tim

    # year_col = [d[:4] for d in subjects['start_date']]
    # year_mon = [d[5:7] for d in subjects['start_date']]

    # subjects['year_col'] = year_col
    # subjects['year_mon'] = year_mon

    # analyze_waiting_time(subjects)
    # analyze_patients_count(subjects)
    # analyze_department_visit(subjects)
    # analyze_department_visit_monthly(subjects)
    # analyze_monthly_patients_visit_by_clinic(subjects)
    # analyze_staff_count_by_clinic(subjects)
    # analyze_waiting_time_by_clinic(subjects)
    # analyze_doctor_patients_count(subjects)

    # context = {
    #     'series_obj': json.dumps(series_obj_p1),
    #     'dis_series_obj': json.dumps(dis_series_obj),
    #     'dis_list': json.dumps(dis_list),
    #     'year_s': json.dumps(year_s),
    #     'year_e': json.dumps(year_e),
    #     'waiting_time_json': waiting_time_json,
    #     'waiting_time_by_clinic': json.dumps(waiting_time_by_clinic),
    #     'patients': patients,
    #     'department_visits': json.dumps(department_visits),
    #     'department_visits_monthly': json.dumps(department_visits_monthly),
    #     'monthly_patient_visit_count': json.dumps(monthly_patient_visit_count),
    #     'staff_count_by_clinic': json.dumps(staff_count),
    #     'doctor_patients_count': json.dumps(doctor_patients_count),
    # }
    context = {
        "office_years": json.dumps(office_years, cls=NpEncoder),
        "office_numbers": json.dumps(office_numbers, cls=NpEncoder),
    }
    # breakpoint()

    return render(request, 'monthly_report/dashboard.html', context)


def top_illness():
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
    # colors = ['#DA726E', '#E7DFAB', '#C5E7AB', '#ABE7D4', '#ABBEE7']
    colors = ['#5B9BD5', '#FFC000', '#A5A5A5', '#EC7D31', '#4472C4']
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

    year_s = year_set[0]
    year_e = year_set[len(year_set) - 1]

    return series_obj_p1, dis_series_obj, dis_list, year_s, year_e


# PRE-REQUISITE FUNCTIONS
# list(a_tim)
def timelist(a_tim):
    a_ret = [to_mins(a) for a in a_tim]
    return a_ret


def to_mins(tim):
    a_1 = float(tim[-5:-3])
    a_2 = float(tim[-2:])
    # print(a_1)
    # print(a_2)
    a_t = a_1 + (a_2 / 60.00)

    # a_t = a_t*60.00
    # print(a_t)
    return a_t


mon_map = [
    'Jan',
    'Feb',
    'Mar',
    'April',
    'May',
    'June',
    'July',
    'August',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]


def con_mon(a_ls):
    mon_map = [
        'Jan',
        'Feb',
        'Mar',
        'April',
        'May',
        'June',
        'July',
        'August',
        'Sep',
        'Oct',
        'Nov',
        'Dec',
    ]
    m_l = []
    for a in a_ls:
        # print(int(a))
        m_l.append(mon_map[int(a) - 1])
    return m_l


mon_map = [
    'Jan',
    'Feb',
    'Mar',
    'April',
    'May',
    'June',
    'July',
    'August',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]

waiting_time_json = ''


def analyze_waiting_time(subjects):
    import numpy as np

    # waiting time stats
    awt = np.sum(subjects['time']) / len(subjects['time'])  # avg. waiting time
    wmn = subjects['time'].min()
    wmx = subjects['time'].max()
    wta = subjects['time'].mean()
    wtm = subjects['time'].median()

    waiting_time = {'min': wmn, 'max': wmx, 'avg': wta, 'median': wtm}
    global waiting_time_json
    waiting_time_json = waiting_time


waiting_time_by_clinic = ''


def analyze_waiting_time_by_clinic(subjects):
    m_ls = set(subjects['year_mon'])
    m_ls = sorted(m_ls)  # conf. if needed
    c_ls = sorted(list(set(subjects['拠点名'])))
    group_clinic_mon = subjects.groupby(['拠点名', 'year_mon']).sum()['time']
    group_clinic_pat = subjects.groupby(['拠点名', 'year_mon']).count()['time']

    m_ls_order = []

    for mon in subjects['year_mon']:
        if mon not in m_ls_order:
            m_ls_order.append(mon)
    m_ls_order.reverse()

    plot5_data = []

    cnt = 0
    for m in m_ls_order:
        m_wise_ls = []
        for c in c_ls:
            m_wise_ls.append(group_clinic_mon[cnt] / group_clinic_pat[cnt])
            cnt += 1
        plot5_data.append({'name': mon_map[int(m) - 1], 'data': m_wise_ls})
    # print(plot5_data)

    order_plot5_data = []
    for mon_o in m_ls_order:
        for data_p in plot5_data:
            if mon_map[int(mon_o) - 1] == data_p['name']:
                order_plot5_data.append(
                    {'name': mon_map[int(mon_o) - 1], 'data': data_p['data']}
                )
    print(m_ls_order)
    print(order_plot5_data)

    global waiting_time_by_clinic
    waiting_time_by_clinic = {'clinics': c_ls, 'data': plot5_data}
    print('>>>>>>>>>>>')
    print(waiting_time_by_clinic)
    print('>>>>>>>>>>>')


patients = ''


def analyze_patients_count(subjects):
    # patients data
    # patients to doctor ratio
    ptdr = len(subjects) / len(set(subjects['staffId']))
    # busy month
    mpis = mon_map[int(subjects['year_mon'].mode()[0])]
    # busy doctor
    mpbd = subjects['姓'].mode()[0]
    tot_pat = len(subjects)
    adm_pat = len(set(subjects['PatientId']))

    global patients

    patients = {
        'total_visit': adm_pat,
        'max_visit_month': mpis,
        'patient_doctor_ratio': ptdr,
        'busiest_doctor': mpbd,
    }


department_visits = ''


def analyze_department_visit(subjects):
    dep_dict = {}
    d_ls = list(set(subjects['診察科']))
    d_ln = len(d_ls)
    for i in range(d_ln):
        dep_dict[d_ls[i]] = len(subjects[subjects['診察科'] == d_ls[i]])

    global department_visits
    department_visits = []
    for val in dep_dict:
        department_visits.append({'name': val, 'y': dep_dict[val]})


department_visits_monthly = ''


def analyze_department_visit_monthly(subjects):
    global department_visits_monthly

    # medical dept. and month wise data
    d_ls = list(set(subjects['診察科']))
    m_ls = []
    for a in subjects['year_mon']:
        if a not in m_ls:
            m_ls.append(a)
    data = {}
    for dp in d_ls:
        p_ls = []
        for mn in m_ls:
            p_ls.append(
                len(
                    subjects.loc[(subjects['診察科'] == dp) & (subjects['year_mon'] == mn)]
                )
            )
        data[dp] = p_ls

    x = [(mon, dep) for mon in m_ls for dep in d_ls]

    y_d = [data[a] for a in d_ls]
    counts = []

    for i in range(len(y_d[0])):
        for j in range(len(y_d)):
            counts.append(y_d[j][i])

    # print(counts)
    m_ls = con_mon(m_ls)  # numeric to months string
    x = [(mon, dep) for mon in m_ls for dep in d_ls]
    series_plot2 = []

    for d in d_ls:
        series_plot2.append({'name': d, 'data': data[d]})
    department_visits_monthly = {
        'months': m_ls,  # [mon_map[int(a)-1] for a in m_ls],
        'data': series_plot2,
    }


monthly_patient_visit_count = ''


def analyze_monthly_patients_visit_by_clinic(subjects):
    global monthly_patient_visit_count

    # clinic, medical base and month wise data
    d_ls = list(set(subjects['拠点名']))
    m_ls = []
    for a in subjects['year_mon']:
        if a not in m_ls:
            m_ls.append(a)
    data = {}
    for dp in d_ls:
        p_ls = []
        for mn in m_ls:
            p_ls.append(
                len(
                    subjects.loc[(subjects['拠点名'] == dp) & (subjects['year_mon'] == mn)]
                )
            )
        data[dp] = p_ls

    x = [(mon, dep) for mon in m_ls for dep in d_ls]

    y_d = [data[a] for a in d_ls]
    counts = []

    for i in range(len(y_d[0])):
        for j in range(len(y_d)):
            counts.append(y_d[j][i])

    # print(counts)
    m_ls = con_mon(m_ls)  # numeric to months string
    x = [(mon, dep) for mon in m_ls for dep in d_ls]
    series_plot2 = []

    for d in d_ls:
        series_plot2.append({'name': d, 'data': data[d]})

    monthly_patient_visit_count = {'months': m_ls, 'data': series_plot2}


staff_count = ''


def analyze_staff_count_by_clinic(subjects):
    global staff_count
    dep_dict = {}  # clinic / medical bases
    d_ls = list(set(subjects['拠点名']))
    d_ln = len(d_ls)
    for i in range(d_ln):
        dep_dict[d_ls[i]] = len(set(subjects[subjects['拠点名'] == d_ls[i]]['staffId']))

    staff_count = []
    for val in dep_dict:
        staff_count.append({'name': val, 'y': dep_dict[val]})


doctor_patients_count = ''


def analyze_doctor_patients_count(subjects):
    global doctor_patients_count
    doct_nam = list(set(subjects['姓']))
    d_hist = list(subjects.groupby('姓').count()['time'])

    doctor_patients_count = [[(a[0]), int(a[1])] for a in list(zip(doct_nam, d_hist))]


def nispottikritto_nothi_yearwise(request):
    load_nisponno_records_table()
    nisponno_records_df = settings.NISPONNO_RECORDS_CSV_FILE_PATH
    nisponno_records_count = nisponno_records_df.groupby('year').size()
    records_numbers = list(nisponno_records_count.values)
    records_years = list(nisponno_records_count.index.values)
    context = {
        'record_numbers': json.dumps(records_numbers, cls=NpEncoder),
        'record_years': json.dumps(records_years, cls=NpEncoder),
    }
    return render(request, 'monthly_report/nispottikritto_nothi_yearwise.html', context)
