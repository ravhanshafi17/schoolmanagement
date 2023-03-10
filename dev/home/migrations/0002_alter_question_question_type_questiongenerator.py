# Generated by Django 4.1.7 on 2023-02-22 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='QuestionGenerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.CharField(max_length=100)),
                ('marks_type', models.IntegerField()),
                ('is_required', models.BooleanField(default=False)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.admin')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.question')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.school')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.teacher')),
            ],
        ),
    ]
