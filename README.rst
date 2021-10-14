=============================
django-composite-auto-field
=============================

.. contents:: A simple Django Field for storing auto-incrementing field. It's useful for storing such as orders code for much easier reading.

----

Installation
------------
Install django-composite-auto-field::

    pip install django-composite-auto-field

Usage
-----
This field uses Django's Aggregate and Max functions to extract the latest code from the database and does a minimum of parsing to calculate the next code. This avoids having to store a counter in the database. Therefore, for correct operation, once the field arguments have been set, it is advisable not to modify them anymore, or to manually act on the codes already calculated and stored in the database.

Import to your models::

    from django_composite_auto_field.fields import CompositeAutoField

Usage::

    class Order(models.Model):
        code = CompositeAutoField(prefix='ORD', use_year=True, zeros=5)

Arguments::

    prefix      # It's used to indicate prefix for the code
    use_year    # When it's True, last two numbers of current year will be used after prefix
    zero        # Indicated number of zeros before the number

Run::

    python manage.py makemigrations
    python manage.py migrate

For example. Using Arguments from above as shown, will result in codes::

    ORD2100001
    ORD2100002
    ORD2100003
    ...

If the year is used, every year the counter will be automatically reset and the count will restart with 1.

Release Notes
-------------
* 0.1.0 - initial release
    - provides CompositeAutoField for storing auto-incrementing field
    - supports Django 3.1 on python 3.6, 3.7, 3.8 and 3.9 - as per the `official django docs <https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_

Todo
----
    - ❌ Create test cases
    - ✔️ Initial release on GitHub
    - ✔️ Initial release on PyPi
    - ❌ Improve last code parsing for make arguments changeable

Contributing
------------
It's an open source project, so any contributions are welcome!