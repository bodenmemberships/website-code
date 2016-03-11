# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdSpeedZonePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('zid', models.PositiveIntegerField(null=True, verbose_name=b'Zone Id', blank=True)),
                ('aid', models.PositiveIntegerField(null=True, verbose_name=b'Ad Id', blank=True)),
                ('num', models.PositiveIntegerField(null=True, verbose_name=b'Number of Ads', blank=True)),
                ('show_errors', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['zid', 'aid'],
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('last_year_paid', models.PositiveIntegerField(null=True, blank=True)),
                ('first_member_date', models.DateField(null=True, blank=True)),
                ('continuous_start_date', models.DateField(null=True, blank=True)),
                ('expected_grad_year', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerClassification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TextPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('txt', ckeditor.fields.RichTextField(max_length=1000, verbose_name=b'Text')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TextWithClass',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('txt', ckeditor.fields.RichTextField(max_length=1000, verbose_name=b'Text')),
                ('cls', models.CharField(max_length=40, verbose_name=b'Class')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Tier1Discipline',
            fields=[
                ('number', models.CharField(unique=True, max_length=12)),
                ('code', models.CharField(max_length=3, serialize=False, primary_key=True)),
                ('long_code', models.CharField(max_length=20, null=True, blank=True)),
                ('name', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TitleBarPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('code', models.CharField(max_length=3, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('active', models.BooleanField(default=True)),
                ('discipline', models.ForeignKey(verbose_name=b'Discipline', to='mainsite.Tier1Discipline')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CustomerAchievements',
            fields=[
                ('customerclassification_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mainsite.CustomerClassification')),
                ('sort_order', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('weight', models.PositiveSmallIntegerField(null=True, blank=True)),
            ],
            bases=('mainsite.customerclassification',),
        ),
        migrations.AddField(
            model_name='customer',
            name='classifications',
            field=models.ManyToManyField(related_name='classification_customers', to='mainsite.CustomerClassification', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='primary_discipline',
            field=models.ForeignKey(related_name='primary_customers', blank=True, to='mainsite.Tier1Discipline', null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='secondary_discipline',
            field=models.ForeignKey(related_name='secondary_customers', blank=True, to='mainsite.Tier1Discipline', null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='subscriptions',
            field=models.ManyToManyField(to='mainsite.CustomerSubscription', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='achievements',
            field=models.ManyToManyField(related_name='achievement_customers', to='mainsite.CustomerAchievements', blank=True),
        ),
    ]
