# Generated by Django 2.1.1 on 2019-08-20 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='收货地址')),
                ('recver', models.CharField(max_length=32, verbose_name='接收人')),
                ('recver_number', models.CharField(max_length=32, verbose_name='邮编')),
                ('recver_phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='接收人电话')),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, verbose_name='用户邮箱')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, verbose_name='联系电话')),
                ('connect_address', models.TextField(blank=True, null=True, verbose_name='联系地址')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品价格')),
                ('goods_total', models.FloatField(verbose_name='商品总价')),
                ('goods_number', models.IntegerField(verbose_name='商品数量')),
                ('goods_picture', models.ImageField(upload_to='buyer/images', verbose_name='商品图片')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('goods_store', models.IntegerField(verbose_name='商品商店')),
                ('user_id', models.IntegerField(verbose_name='用户id')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=32, verbose_name='id订单编号')),
                ('goods_count', models.IntegerField(verbose_name='商品数量')),
                ('order_price', models.FloatField(verbose_name='订单总价')),
                ('order_status', models.IntegerField(default=1, verbose_name='订单状态')),
                ('order_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Buyer.Address', verbose_name='订单地址')),
                ('order_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer', verbose_name='订单用户')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_id', models.IntegerField(verbose_name='商品id')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品价格')),
                ('goods_number', models.IntegerField(verbose_name='商品购买数量')),
                ('goods_total', models.FloatField(verbose_name='商品总价')),
                ('goods_store', models.IntegerField(verbose_name='商品id')),
                ('goods_image', models.ImageField(default='static/buyer/images/Store.jpg', upload_to='', verbose_name='商品图片')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Order', verbose_name='订单编号')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='buyer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.Buyer', verbose_name='用户id'),
        ),
    ]
