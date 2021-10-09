=============================
django-composite-auto-field
=============================

.. contents:: A simple Django Field for storing auto-incrementing field. It's useful for storing such as orders code for much easier reading.

----

Installation
----------
Install django-composite-auto-field::

    pip install django-composite-auto-field

Usage
----------
Import to your models::

    from django-composite-auto-field.models.fields import CompositeAutoField

Usage::

    class Order(models.Model):
        code = CompositeAutoField(prefix='ORD', use_year=True, zeros=5)

