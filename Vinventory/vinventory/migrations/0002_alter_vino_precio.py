# Generated by Django 3.2.18 on 2023-05-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vino',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
