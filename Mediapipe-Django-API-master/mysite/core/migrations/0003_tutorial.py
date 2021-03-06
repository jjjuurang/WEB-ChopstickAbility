# Generated by Django 4.0.4 on 2022-05-30 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0002_delete_book_alter_image_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('NAME', models.OneToOneField(db_column='username', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('STEP1', models.IntegerField(default=0)),
                ('STEP2', models.IntegerField(default=0)),
                ('STEP3', models.IntegerField(default=0)),
                ('STEP4', models.IntegerField(default=0)),
            ],
        ),
    ]
