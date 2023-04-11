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

    prefix      # It's used to indicate prefix for the code, default is "CC"
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
If you pass a string to the field, it will be used instead of the generated value. Pay attention to the passed values, they will be used for the generation of subsequent values.

Tests
-------------
To run tests::

    # clone this repository on your PC

    # create the virtual environment
    python -m venv venv

    # activate the virtual environment
    source venv\bin\activate

    # installa requirements
    pip install -r .\requirements.txt

    # run tests
    python manage.py test

Release Notes
-------------
* 0.1.3
    - added tests
    - added support for custom string as argument
    - added support for Django 4.2 on python 3.8, 3.9, 3.10 and 3.11 - as per the `official django docs <https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_
* 0.1.2
    - fixed year change
* 0.1.1 - initial release
    - provides CompositeAutoField for storing auto-incrementing field
    - supports Django 3.1 on python 3.6, 3.7, 3.8 and 3.9 - as per the `official django docs <https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_

Contributing
------------
It's an open source project, so any contributions are welcome!