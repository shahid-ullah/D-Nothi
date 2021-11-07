# monthly_report/serializers.py
from rest_framework import serializers

from .models import MonthModel, ReportModel, YearModel


class YearModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearModel
        fields = ["id", "year"]


class MonthModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthModel
        fields = ["id", "month"]


class ReportModelSerializer(serializers.ModelSerializer):
    year = YearModelSerializer()
    month = MonthModelSerializer()

    class Meta:
        model = ReportModel
        fields = "__all__"
