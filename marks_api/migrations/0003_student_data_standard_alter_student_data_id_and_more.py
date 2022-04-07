# Generated by Django 4.0.3 on 2022-04-07 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marks_api', '0002_rename_student_student_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_data',
            name='standard',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student_data',
            name='id',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student_data',
            name='marks',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='student_data',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]