# Generated by Django 4.0.1 on 2022-02-06 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
