# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexInTimeList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, verbose_name='\u4ee3\u7801')),
                ('name', models.CharField(max_length=20, verbose_name='\u540d\u79f0')),
                ('change', models.DecimalField(verbose_name='\u6da8\u8dcc\u5e45', max_digits=7, decimal_places=4)),
                ('open', models.DecimalField(verbose_name='\u5f00\u76d8\u70b9\u4f4d', max_digits=10, decimal_places=4)),
                ('preclose', models.DecimalField(verbose_name='\u6628\u65e5\u6536\u76d8', max_digits=10, decimal_places=4)),
                ('close', models.DecimalField(verbose_name='\u6536\u76d8\u70b9\u4f4d', max_digits=10, decimal_places=4)),
                ('high', models.DecimalField(verbose_name='\u6700\u9ad8\u70b9\u4f4d', max_digits=10, decimal_places=4)),
                ('low', models.DecimalField(verbose_name='\u6700\u4f4e\u70b9\u4f4d', max_digits=10, decimal_places=4)),
                ('volume', models.BigIntegerField(verbose_name='\u6210\u4ea4\u91cf\uff08\u624b\uff09')),
                ('amount', models.DecimalField(verbose_name='\u6210\u4ea4\u91d1\u989d\uff08\u4ebf\u5143\uff09', max_digits=14, decimal_places=4)),
            ],
            options={
                'db_table': 'index_in_time',
                'verbose_name': '\u5927\u76d8\u6307\u6570\u5b9e\u65f6',
            },
        ),
    ]
