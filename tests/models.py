from django.db import models

from django_composite_auto_field.fields import CompositeAutoField


class TestModelA(models.Model):
    custom_code = CompositeAutoField(prefix='AA', use_year=True, zeros=4)


class TestModelB(models.Model):
    custom_code = CompositeAutoField(prefix='BB', use_year=False, zeros=5)
