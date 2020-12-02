# Generated by Django 3.1.2 on 2020-12-01 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apellido', models.CharField(max_length=25)),
                ('nombre', models.CharField(max_length=25)),
                ('documento', models.CharField(max_length=8)),
                ('obra_social', models.CharField(max_length=30)),
                ('medico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Médico')),
            ],
        ),
    ]
