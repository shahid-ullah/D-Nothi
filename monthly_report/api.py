# monthly_report/api.py
from datetime import datetime

from rest_framework import generics

from .models import ReportModel
from .serializers import ReportModelSerializer


class ReportListAPI(generics.ListAPIView):
    queryset = ReportModel.objects.all()
    serializer_class = ReportModelSerializer

    def get(self, request, *args, **kwargs):
        year = kwargs.get('query_year')
        if year:
            self.queryset = ReportModel.objects.filter(year__year=year)
        else:
            date = datetime.now()
            year = date.year
            self.queryset = ReportModel.objects.filter(year__year=year)
        return self.list(request, *args, **kwargs)
