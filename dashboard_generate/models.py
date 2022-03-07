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
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_total_offices"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportNispottikrittoNothiModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_nispottikritto_nothi"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportUpokarvogiModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_upokarvogi"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportPotrojariModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_potrojair"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportNoteNisponnoModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_note_nisponno"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportTotalUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_total_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportMaleNothiUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_male_nothi_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportFemaleNothiUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_female_nothi_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportMobileAppUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_mobile_app_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportAndroidUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_android_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportIOSUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_ios_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


def empty_dictionary():
    return {}


class ReportLoginTotalUsers(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    employee_record_ids = models.JSONField(default=empty_dictionary)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_login_total_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportLoginMalelUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    employee_record_ids = models.JSONField(default=empty_dictionary)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_login_male_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class ReportLoginFemalelUsersModel(models.Model):
    year_month_day = models.CharField(
        max_length=100, blank=False, null=False, db_index=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    year = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    month = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    day = models.PositiveIntegerField(blank=False, null=False, db_index=True)
    count_or_sum = models.PositiveIntegerField(default=0)
    employee_record_ids = models.JSONField(default=empty_dictionary)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    report_date = models.CharField(max_length=100)
    report_day = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "report_login_female_users"

    def __str__(self):
        return f'year: {self.year} month: {self.month}, day: {self.day}, count_or_sum: {self.count_or_sum}'


class DashboardUpdateLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    status = models.JSONField(default=empty_dictionary)
    update_start_time = models.DateTimeField(blank=True, null=True)
    update_completion_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "dashboard_update_log"
        ordering = ['-id']
