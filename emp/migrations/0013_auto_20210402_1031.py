# Generated by Django 3.1.7 on 2021-04-02 10:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0012_auto_20210401_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intimemodel',
            name='City',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='intimemodel',
            name='ip',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='DateOfJoin',
            field=models.DateField(default=datetime.datetime(2021, 4, 2, 10, 31, 6, 502356)),
        ),
    ]
