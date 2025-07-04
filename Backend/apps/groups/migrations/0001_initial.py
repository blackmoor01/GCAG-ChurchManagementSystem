# Generated by Django 5.2.2 on 2025-06-12 07:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('ministry_type', models.CharField(choices=[('PASTORAL', 'Pastoral Care'), ('WORSHIP', 'Worship & Music'), ('YOUTH', 'Youth Ministry'), ('CHILDREN', 'Children Ministry'), ('EVANGELISM', 'Evangelism & Outreach'), ('EDUCATION', 'Christian Education'), ('FELLOWSHIP', 'Fellowship & Community'), ('MISSIONS', 'Missions & Service'), ('ADMIN', 'Administration'), ('MEDIA', 'Media & Technology'), ('CHOIR', 'Choir'), ('USHER', 'Ushering'), ('FIN', 'Finance'), ('PRAY', 'Prayer'), ('WOMEN', 'Women'), ('MEN', 'Men'), ('YS', 'Young Singles')], max_length=20)),
                ('group_type', models.CharField(choices=[('SMALL_GROUP', 'Small Group'), ('MINISTRY_TEAM', 'Ministry Team'), ('BIBLE_STUDY', 'Bible Study'), ('PRAYER_GROUP', 'Prayer Group'), ('SERVICE_TEAM', 'Service Team'), ('CHOIR', 'Choir'), ('COMMITTEE', 'Committee')], default='SMALL_GROUP', max_length=20)),
                ('meeting_schedule', models.JSONField(default=dict)),
                ('meeting_location', models.CharField(blank=True, max_length=200)),
                ('max_capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_open_to_new_members', models.BooleanField(default=True)),
                ('requires_approval', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_groups', to=settings.AUTH_USER_MODEL)),
                ('leaders', models.ManyToManyField(blank=True, related_name='led_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GroupMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('date', models.DateTimeField()),
                ('location', models.CharField(blank=True, max_length=200)),
                ('duration_minutes', models.PositiveIntegerField(default=60)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('cancellation_reason', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to='groups.group')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('date_left', models.DateField(blank=True, null=True)),
                ('role', models.CharField(choices=[('MEMBER', 'Member'), ('LEADER', 'Leader'), ('CO_LEADER', 'Co-Leader'), ('ASSISTANT', 'Assistant Leader')], default='MEMBER', max_length=20)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('PENDING', 'Pending Approval'), ('REMOVED', 'Removed')], default='ACTIVE', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('added_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='added_memberships', to=settings.AUTH_USER_MODEL)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_joined'],
                'unique_together': {('member', 'group')},
            },
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='member_groups', through='groups.GroupMembership', through_fields=('group', 'member'), to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='GroupAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recorded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recorded_attendance', to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='groups.groupmeeting')),
            ],
            options={
                'unique_together': {('meeting', 'member')},
            },
        ),
    ]
