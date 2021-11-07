# monthly_report/models.py
import uuid

from django.conf import settings
from django.db import models


class TableNameModel(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"table name: {self.name}"


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.table_name.name, filename)


class CSVDataStorageModel(models.Model):
    table_name = models.ForeignKey(TableNameModel, on_delete=models.CASCADE)
    file_name = models.FileField(upload_to=user_directory_path)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"file: {self.file_name}"


class YearModel(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"year: {self.year}"


class MonthModel(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    month = models.PositiveSmallIntegerField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"month: {self.month}"


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
