# Generated by Django 3.2.8 on 2021-10-11 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('downloader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt', models.DateTimeField(auto_now_add=True)),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='downloader.video')),
            ],
        ),
    ]