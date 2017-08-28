# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HorseBasic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, verbose_name='\u4ee3\u7801')),
                ('name', models.CharField(max_length=20, verbose_name='\u540d\u79f0')),
                ('industry', models.CharField(max_length=50, verbose_name='\u6240\u5c5e\u884c\u4e1a')),
                ('area', models.CharField(default='\u672a\u77e5', max_length=50, null=True, verbose_name='\u5730\u533a')),
                ('pe', models.DecimalField(verbose_name='\u5e02\u76c8\u7387', max_digits=14, decimal_places=4)),
                ('outstanding', models.DecimalField(verbose_name='\u6d41\u901a\u80a1\u672c\uff08\u4ebf\uff09', max_digits=14, decimal_places=4)),
                ('totals', models.DecimalField(verbose_name='\u603b\u80a1\u672c\uff08\u4ebf\uff09', max_digits=14, decimal_places=4)),
                ('totalAssets', models.DecimalField(verbose_name='\u603b\u8d44\u4ea7\uff08\u4e07\uff09', max_digits=14, decimal_places=4)),
                ('liquidAssets', models.DecimalField(verbose_name='\u6d41\u52a8\u8d44\u4ea7', max_digits=14, decimal_places=4)),
                ('fixedAssets', models.DecimalField(verbose_name='\u56fa\u5b9a\u8d44\u4ea7', max_digits=14, decimal_places=4)),
                ('reserved', models.DecimalField(verbose_name='\u516c\u79ef\u91d1', max_digits=14, decimal_places=4)),
                ('reservedPerShare', models.DecimalField(verbose_name='\u6bcf\u80a1\u516c\u79ef\u91d1', max_digits=14, decimal_places=4)),
                ('esp', models.DecimalField(verbose_name='\u6bcf\u80a1\u6536\u76ca', max_digits=7, decimal_places=4)),
                ('bvps', models.DecimalField(verbose_name='\u6bcf\u80a1\u51c0\u8d44', max_digits=14, decimal_places=4)),
                ('pb', models.DecimalField(verbose_name='\u5e02\u51c0\u7387', max_digits=14, decimal_places=4)),
                ('timeToMarket', models.BigIntegerField(verbose_name='\u4e0a\u5e02\u65e5\u671f')),
                ('undp', models.DecimalField(verbose_name='\u672a\u5206\u5229\u6da6', max_digits=14, decimal_places=4)),
                ('perundp', models.DecimalField(verbose_name='\u6bcf\u80a1\u672a\u5206', max_digits=7, decimal_places=4)),
                ('rev', models.DecimalField(verbose_name='\u6536\u5165\u540c\u6bd4\uff08%\uff09', max_digits=14, decimal_places=4)),
                ('profit', models.DecimalField(verbose_name='\u5229\u6da6\u540c\u6bd4\uff08%\uff09', max_digits=14, decimal_places=4)),
                ('gpr', models.DecimalField(verbose_name='\u6bdb\u5229\u7387\uff08%\uff09', max_digits=7, decimal_places=4)),
                ('npr', models.DecimalField(verbose_name='\u51c0\u5229\u6da6\u7387\uff08%\uff09', max_digits=10, decimal_places=4)),
                ('holders', models.BigIntegerField(verbose_name='\u80a1\u4e1c\u4eba\u6570')),
            ],
            options={
                'db_table': 'horse_basic',
                'verbose_name': '\u80a1\u7968\u57fa\u672c\u4fe1\u606f\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='HorseBasicBackup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=10, verbose_name='\u4ee3\u7801')),
                ('name', models.CharField(max_length=20, verbose_name='\u540d\u79f0')),
                ('industry', models.CharField(max_length=50, verbose_name='\u6240\u5c5e\u884c\u4e1a')),
                ('area', models.CharField(default='\u672a\u77e5', max_length=50, null=True, verbose_name='\u5730\u533a')),
                ('pe', models.DecimalField(verbose_name='\u5e02\u76c8\u7387', max_digits=14, decimal_places=4)),
                ('outstanding', models.DecimalField(verbose_name='\u6d41\u901a\u80a1\u672c\uff08\u4ebf\uff09', max_digits=14, decimal_places=4)),
                ('totals', models.DecimalField(verbose_name='\u603b\u80a1\u672c\uff08\u4ebf\uff09', max_digits=14, decimal_places=4)),
                ('totalAssets', models.DecimalField(verbose_name='\u603b\u8d44\u4ea7\uff08\u4e07\uff09', max_digits=14, decimal_places=4)),
                ('liquidAssets', models.DecimalField(verbose_name='\u6d41\u52a8\u8d44\u4ea7', max_digits=14, decimal_places=4)),
                ('fixedAssets', models.DecimalField(verbose_name='\u56fa\u5b9a\u8d44\u4ea7', max_digits=14, decimal_places=4)),
                ('reserved', models.DecimalField(verbose_name='\u516c\u79ef\u91d1', max_digits=14, decimal_places=4)),
                ('reservedPerShare', models.DecimalField(verbose_name='\u6bcf\u80a1\u516c\u79ef\u91d1', max_digits=14, decimal_places=4)),
                ('esp', models.DecimalField(verbose_name='\u6bcf\u80a1\u6536\u76ca', max_digits=7, decimal_places=4)),
                ('bvps', models.DecimalField(verbose_name='\u6bcf\u80a1\u51c0\u8d44', max_digits=14, decimal_places=4)),
                ('pb', models.DecimalField(verbose_name='\u5e02\u51c0\u7387', max_digits=14, decimal_places=4)),
                ('timeToMarket', models.BigIntegerField(verbose_name='\u4e0a\u5e02\u65e5\u671f')),
                ('undp', models.DecimalField(verbose_name='\u672a\u5206\u5229\u6da6', max_digits=14, decimal_places=4)),
                ('perundp', models.DecimalField(verbose_name='\u6bcf\u80a1\u672a\u5206', max_digits=7, decimal_places=4)),
                ('rev', models.DecimalField(verbose_name='\u6536\u5165\u540c\u6bd4\uff08%\uff09', max_digits=14, decimal_places=4)),
                ('profit', models.DecimalField(verbose_name='\u5229\u6da6\u540c\u6bd4\uff08%\uff09', max_digits=14, decimal_places=4)),
                ('gpr', models.DecimalField(verbose_name='\u6bdb\u5229\u7387\uff08%\uff09', max_digits=7, decimal_places=4)),
                ('npr', models.DecimalField(verbose_name='\u51c0\u5229\u6da6\u7387\uff08%\uff09', max_digits=10, decimal_places=4)),
                ('holders', models.BigIntegerField(verbose_name='\u80a1\u4e1c\u4eba\u6570')),
            ],
            options={
                'db_table': 'horse_basic_backup',
                'verbose_name': '\u80a1\u7968\u57fa\u672c\u4fe1\u606f\u5217\u8868\u5907\u4efd',
            },
        ),
    ]
