# Generated by Django 2.1.1 on 2019-07-24 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0003_auto_20190723_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_description',
            field=models.TextField(max_length=32, verbose_name='商品描述'),
        ),
    ]