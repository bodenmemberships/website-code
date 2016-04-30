# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpeLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('external_url', models.URLField(help_text='e.g. http://example.com/thank-you', verbose_name='External URL', blank=True)),
            ],
            options={
                'ordering': ['category__title', 'title'],
                'verbose_name': 'link',
            },
        ),
        migrations.CreateModel(
            name='SpeLinkCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=255)),
                ('class_name', models.CharField(max_length=255, null=True, blank=True)),
                ('show_all_external', models.URLField(help_text='e.g. http://example.com/thank-you', verbose_name='Show all - External URL', blank=True)),
                ('show_all_page', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms.Page', help_text='A page has priority over an external URL', null=True, verbose_name='Show all - Page URL')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='SpeLinkPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('category', models.ForeignKey(to='spe_links.SpeLinkCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='spelink',
            name='category',
            field=models.ForeignKey(to='spe_links.SpeLinkCategory', null=True),
        ),
        migrations.AddField(
            model_name='spelink',
            name='page_url',
            field=cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms.Page', help_text='A page has priority over an external URL', null=True, verbose_name='Page URL'),
        ),
    ]
