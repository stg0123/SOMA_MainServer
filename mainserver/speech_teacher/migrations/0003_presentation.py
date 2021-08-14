# Generated by Django 3.2.5 on 2021-08-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speech_teacher', '0002_st_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presentation',
            fields=[
                ('presentation_id', models.AutoField(primary_key=True, serialize=False)),
                ('presentation_title', models.CharField(max_length=20)),
                ('presentation_time', models.IntegerField()),
                ('presentation_date', models.DateField()),
                ('presentation_update_date', models.DateTimeField(auto_now=True)),
                ('presentation_ex_dupword', models.TextField(null=True)),
                ('presentation_ex_improper', models.TextField(null=True)),
            ],
            options={
                'db_table': 'presentation',
                'managed': False,
            },
        ),
    ]
