# Generated by Django 3.2 on 2024-01-31 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsstatus',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]