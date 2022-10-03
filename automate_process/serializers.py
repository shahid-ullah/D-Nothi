from backup_source_db.models import BackupDBLog
from dashboard_generate.models import ReportGenerationLog
from rest_framework import serializers

from .models import SourceDBLog


class DatabaseBackupLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDBLog
        fields = "__all__"


class ReportGenerationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportGenerationLog
        fields = "__all__"


class SourceDBLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceDBLog
        fields = "__all__"


class BackupDBLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupDBLog
        fields = "__all__"
