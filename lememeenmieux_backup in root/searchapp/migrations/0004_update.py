# Generated by Django 2.0.4 on 2018-07-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchapp', '0003_product_imagelink'),
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastUpdate', models.DateField()),
                ('Comment', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]