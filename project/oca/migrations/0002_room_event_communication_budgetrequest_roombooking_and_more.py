# Generated by Django 5.1.3 on 2024-11-10 16:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oca', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('approval_notes', models.TextField(blank=True, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='oca.club_panel')),
            ],
        ),
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communications', to='oca.event')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_requested', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount_approved', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('approval_notes', models.TextField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget_requests', to='oca.event')),
            ],
        ),
        migrations.CreateModel(
            name='RoomBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_bookings', to='oca.event')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oca.room')),
            ],
        ),
        migrations.CreateModel(
            name='EventReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_live', models.BooleanField(default=False)),
                ('summary', models.TextField()),
                ('participation_count', models.IntegerField()),
                ('total_budget_used', models.DecimalField(decimal_places=2, max_digits=10)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='oca.event')),
                ('room_booking_details', models.ManyToManyField(related_name='reports', to='oca.roombooking')),
            ],
        ),
    ]