# Generated by Django 5.1.1 on 2024-11-14 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_category_tag_remove_form_categories_remove_form_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='form',
            name='receiver_signature',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
