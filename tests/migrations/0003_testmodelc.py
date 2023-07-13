# Generated by Django 4.2 on 2023-07-13 16:18

from django.db import migrations, models
import django_composite_auto_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_alter_testmodelb_custom_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModelC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_code', django_composite_auto_field.fields.CompositeAutoField(max_length=250, prefix='CCC', use_year=True)),
            ],
        ),
    ]
