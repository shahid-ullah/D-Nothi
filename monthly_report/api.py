# monthly_report/api.py
from datetime import datetime

from rest_framework import generics

from .models import ReportModel, YearModel
from .serializers import ReportModelSerializer


class ReportListAPI(generics.ListAPIView):
    queryset = ReportModel.objects.all()
    serializer_class = ReportModelSerializer

    def get(self, request, *args, **kwargs):
        year = kwargs.get('query_year')
        if year:
            self.queryset = ReportModel.objects.filter(year__year=year)
        else:
            years_objects = YearModel.objects.all()
            years_list = [obj.year for obj in years_objects]
            recent_year = max(years_list)
            self.queryset = ReportModel.objects.filter(year__year=recent_year)
        return self.list(request, *args, **kwargs)
