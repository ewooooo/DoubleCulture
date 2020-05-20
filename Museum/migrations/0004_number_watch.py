# Generated by Django 2.2.12 on 2020-05-01 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Museum', '0003_delete_watch_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='number_watch',
            fields=[
                ('name', models.CharField(max_length=10)),
                ('student_number', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('howmany', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['student_number'],
            },
        ),
    ]