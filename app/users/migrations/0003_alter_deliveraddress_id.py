# Generated by Django 5.0.3 on 2024-03-28 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_deliveraddress_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveraddress',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
