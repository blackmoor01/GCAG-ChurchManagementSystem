# Generated by Django 5.2.2 on 2025-06-10 13:10

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('mfa_enabled', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('MEMBER', 'Member'), ('HEAD_PASTOR', 'Head Pastor')], default='MEMBER', max_length=20)),
                ('member_id', models.CharField(blank=True, max_length=20, unique=True)),
                ('ministry', models.CharField(blank=True, choices=[('CHOIR', 'Choir'), ('USHER', 'Ushering'), ('FIN', 'Finance'), ('PRAY', 'Prayer'), ('YOUTH', 'Youth'), ('WOMEN', 'Women'), ('MEN', 'Men'), ('CHILD', 'Children'), ('YS', 'Young Singles')], max_length=10, null=True)),
                ('membership_start_date', models.DateField(default=django.utils.timezone.now)),
                ('baptized', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10)),
                ('address', models.TextField(blank=True)),
                ('login_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('registration_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('last_login_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
