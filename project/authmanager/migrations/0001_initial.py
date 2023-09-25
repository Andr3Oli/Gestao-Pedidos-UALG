# Generated by Django 4.1.7 on 2023-05-21 17:27

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculdade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(db_column='nome', max_length=255)),
            ],
            options={
                'db_table': 'Faculdade',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Utilizador',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('contacto', phonenumber_field.modelfields.PhoneNumberField(max_length=20, region=None)),
                ('valido', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'Utilizador',
                'managed': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(db_column='nome', max_length=255)),
                ('faculdadeid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authmanager.faculdade')),
            ],
            options={
                'db_table': 'Departamento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProfessorUniversitario',
            fields=[
                ('utilizador_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authmanager.utilizador')),
                ('gabinete', models.CharField(db_column='Gabinete', max_length=255)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authmanager.departamento')),
                ('faculdade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authmanager.faculdade')),
            ],
            options={
                'db_table': 'ProfessorUniversitario',
                'managed': True,
            },
            bases=('authmanager.utilizador',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('utilizador_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='authmanager.utilizador')),
                ('gabinete', models.CharField(db_column='Gabinete', max_length=255)),
                ('faculdade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authmanager.faculdade')),
            ],
            options={
                'db_table': 'Funcionario',
                'managed': True,
            },
            bases=('authmanager.utilizador',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]