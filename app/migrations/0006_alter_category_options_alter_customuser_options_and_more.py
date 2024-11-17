# Generated by Django 5.1.1 on 2024-11-14 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_delete_user_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterModelOptions(
            name='form',
            options={'verbose_name': 'Form', 'verbose_name_plural': 'Forms'},
        ),
        migrations.AlterModelOptions(
            name='formversion',
            options={'verbose_name': 'Form Version', 'verbose_name_plural': 'Form Versions'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterField(
            model_name='form',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='forms', to='app.category'),
        ),
        migrations.AlterField(
            model_name='form',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='forms', to='app.tag'),
        ),
        migrations.AlterField(
            model_name='formversion',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='app.form'),
        ),
    ]
