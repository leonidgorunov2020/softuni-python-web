# Generated by Django 3.2.12 on 2022-04-07 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20220407_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Template', 'Template'), ('Plugin', 'Plugin'), ('Module', 'Module'), ('Other', 'Other')], max_length=8),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
