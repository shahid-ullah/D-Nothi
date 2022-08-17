from rest_framework import serializers
from .models import TrackSourceDBLastFetchTime

class DatabaseBackupLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackSourceDBLastFetchTime
        fields = "__all__"