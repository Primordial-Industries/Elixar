# Generated by Django 3.1.1 on 2020-09-06 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PayApp', '0003_student_verif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
