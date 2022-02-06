# dashboard_generate/models.py


from django.conf import settings
from django.db import models


class ReportTotalOfficesModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False)
    month = models.PositiveIntegerField(blank=False, null=False)
    day = models.PositiveIntegerField(blank=False, null=False)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_total_offices"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'
