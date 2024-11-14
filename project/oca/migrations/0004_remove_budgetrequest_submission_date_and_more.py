# Generated by Django 5.1.3 on 2024-11-11 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oca', '0003_remove_communication_event_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budgetrequest',
            name='submission_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.AddField(
            model_name='budgetrequest',
            name='budget_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
