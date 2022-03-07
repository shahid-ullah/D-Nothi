# dashboard_generate/serializers.py
from rest_framework import serializers

from .models import DashboardUpdateLog


class DashboardUpdateLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardUpdateLog
        fields = "__all__"
