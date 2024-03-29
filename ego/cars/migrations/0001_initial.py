# Generated by Django 4.2 on 2024-03-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_type', models.CharField(choices=[('Autos', 'Autos'), ('Pickups y Comerciales', 'Pickaups Y Comerciales'), ('SUVs y Crossovers', 'Suvs Y Crossovers')], max_length=50)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'unique_together': {('car_type', 'model', 'year')},
            },
        ),
    ]
