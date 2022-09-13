from rest_framework import serializers

from backup_source_db.models import BackupDBLog
from .models import SourceDBLog, TrackSourceDBLastFetchTime

class DatabaseBackupLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDBLog
        fields = "__all__"

class SourceDBLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDBLog
        fields = "__all__"

class BackupDBLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupDBLog
        fields = "__all__"
