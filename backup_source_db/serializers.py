from rest_framework import serializers

from .models import BackupOffices


class OfficesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupOffices
        fields = ['source_id', 'office_name_eng']
