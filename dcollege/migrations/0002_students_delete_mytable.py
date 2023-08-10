# Generated by Django 4.1.5 on 2023-03-05 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcollege', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', max_length=30)),
                ('password', models.CharField(db_column='password', max_length=10)),
            ],
            options={
                'db_table': 'student',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='MyTable',
        ),
    ]
