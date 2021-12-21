# Generated by Django 3.1.6 on 2021-12-21 19:16

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MedicalExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('name', models.CharField(max_length=80)),
                ('medic', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='UserApp.medic')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation', models.CharField(max_length=100)),
                ('kinship', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular person', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('cpf', models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_CPF', message='CPF must be valid', regex='^([0-9]{2}[\\.]?[0-9]{3}[\\.]?[0-9]{3}[\\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\\.]?[0-9]{3}[\\.]?[0-9]{3}[-]?[0-9]{2})$')])),
                ('birt_date', models.DateField()),
                ('civil_state', models.CharField(choices=[('S', 'Sigle'), ('M', 'Married'), ('D', 'Divorced')], default='S', max_length=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='UserApp.person')),
                ('phoneNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Father',
            fields=[
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='UserApp.person')),
                ('occupation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular user', primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('MED', 'medic'), ('ADM', 'administrator'), ('PAT', 'patient'), ('AUD', 'auditor')], default='PAT', max_length=15)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ReagentExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('NR', 'Not reagent'), ('R', 'Reagent')], max_length=2)),
                ('exam', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UserApp.medicalexam')),
            ],
        ),
        migrations.CreateModel(
            name='Prenatal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('medic', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='medic', to='UserApp.medic')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='UserApp.patient')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UserApp.person'),
        ),
        migrations.AddField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='OtherExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=200)),
                ('exam', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UserApp.medicalexam')),
            ],
        ),
        migrations.CreateModel(
            name='NumericMedicalExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('exam', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UserApp.medicalexam')),
            ],
        ),
        migrations.AddField(
            model_name='medicalexam',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='UserApp.person'),
        ),
        migrations.AddField(
            model_name='medic',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UserApp.person'),
        ),
        migrations.AddField(
            model_name='medic',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('weight', models.FloatField()),
                ('date', models.DateField()),
                ('ig', models.CharField(max_length=80)),
                ('pa', models.CharField(max_length=80)),
                ('edema', models.CharField(max_length=80)),
                ('av', models.CharField(max_length=80)),
                ('bcf', models.CharField(max_length=80)),
                ('complication', models.CharField(max_length=200)),
                ('cd', models.CharField(max_length=80)),
                ('substance_use', models.CharField(max_length=200)),
                ('prenatal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.prenatal')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('zipcode', models.IntegerField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserApp.person')),
            ],
        ),
    ]
