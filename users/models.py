# users/models.py
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    username_eng = models.CharField(blank=True, max_length=100)
    username_bng = models.CharField(blank=True, max_length=100)
    personal_email = models.EmailField(blank=True)
    personal_mobile = models.CharField(blank=True, max_length=100)
    office_name_eng = models.CharField(blank=True, max_length=100)
    office_name_bng = models.CharField(blank=True, max_length=100)
    designation = models.CharField(blank=True, max_length=100)
    nid = models.CharField(blank=True, max_length=50)
    date_of_birth = models.CharField(blank=True, max_length=50)
    active = models.BooleanField(default=True)
    father_name_eng = models.CharField(blank=True, max_length=100)
    father_name_bng = models.CharField(blank=True, max_length=100)
    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        '''On save, update timestamps'''
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username_eng
