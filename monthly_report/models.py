# monthly_report/models.py
import uuid
from datetime import datetime

from django.conf import settings
from django.db import models

# class DataframeRecord(models.Model):
#     dataframe_name = models.CharField(max_length=50, unique=True)
#     creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created']

#     def __str__(self):
#         return f"dataframe name: {self.dataframe_name}"


class ReportTypeModel(models.Model):
    type_name = models.CharField(max_length=50, unique=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"type: {self.type_name}"


def gdjd_upload_path(instance, filename):
    now = datetime.now()
    current_day = str(now.year) + "_" + str(now.month) + "_" + str(now.day)

    return '{0}/{1}/{2}'.format(instance.report_type.type_name, current_day, filename)


# class CSVDataStorageModel(models.Model):
#     dataframe = models.ForeignKey(DataframeRecord, on_delete=models.CASCADE)
#     file_name = models.FileField(upload_to=upload_path)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"file: {self.dataframe.dataframe_name}"

#     class Meta:
#         ordering = ['-created']
class GeneralDrilldownJSONDataModel(models.Model):
    report_type = models.ForeignKey(ReportTypeModel, on_delete=models.CASCADE)
    file_name = models.FileField(upload_to=gdjd_upload_path)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"file: {self.report_type.type_name}"

    class Meta:
        ordering = ['-created']


class YearModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year}"


class MonthModel(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    month = models.PositiveSmallIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.month}"


class ReportModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.ForeignKey(
        YearModel, related_name="reports_full_year", on_delete=models.CASCADE
    )
    month = models.ForeignKey(
        MonthModel, related_name="reports", on_delete=models.CASCADE
    )
    total_office = models.PositiveIntegerField(blank=True, null=True)
    nispotti_krito_nothi = models.PositiveIntegerField(blank=True, null=True)
    total_upokarvogi = models.PositiveIntegerField(blank=True, null=True)
    total_users = models.PositiveIntegerField(blank=True, null=True)
    total_nothi_users_male = models.PositiveIntegerField(blank=True, null=True)
    total_nothi_users_female = models.PositiveIntegerField(blank=True, null=True)
    total_mobile_app_users = models.PositiveIntegerField(blank=True, null=True)
    total_nisponno = models.PositiveIntegerField(blank=True, null=True)
    total_potrojari = models.PositiveIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['year', 'month'], name='year_month')
        ]

    def __str__(self):
        return f"{self.year}, {self.month}"


class TableNameModel(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


def file_upload_path(instance, filename):
    now = datetime.now()
    current_day = str(now.year) + "_" + str(now.month) + "_" + str(now.day)

    return '{0}/{1}/{2}'.format(instance.table_name.name, current_day, filename)


class ReportStorageModel(models.Model):
    table_name = models.ForeignKey(TableNameModel, on_delete=models.CASCADE)
    file_name = models.FileField(upload_to=file_upload_path)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.table_name.name} {self.file_name}'
