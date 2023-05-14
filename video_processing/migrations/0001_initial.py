# Generated by Django 4.1.9 on 2023-05-14 18:26

from django.db import migrations, models
import ecowiser.storage_backend


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video_file', models.FileField(storage=ecowiser.storage_backend.B2Storage(), upload_to='videos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]