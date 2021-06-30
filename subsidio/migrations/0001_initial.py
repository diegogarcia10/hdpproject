# Generated by Django 3.2.4 on 2021-06-29 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DUI', models.CharField(max_length=20)),
                ('NIT', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_departamento', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TipoSubsidio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo_subsidio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_zona', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_municipio', models.CharField(max_length=50)),
                ('codigo_departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsidio.departamento')),
            ],
        ),
        migrations.AddField(
            model_name='departamento',
            name='codigo_zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subsidio.zona'),
        ),
        migrations.CreateModel(
            name='BeneficiarioTipoSubsidio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=5, max_digits=10)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('codigo_beneficiario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subsidio.beneficiario')),
                ('codigo_subsidio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subsidio.tiposubsidio')),
            ],
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='codigo_municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='subsidio.municipio'),
        ),
        migrations.AddField(
            model_name='beneficiario',
            name='codigo_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
