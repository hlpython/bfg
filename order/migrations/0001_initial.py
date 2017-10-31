# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_recordbrowse'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('detail_name', models.CharField(max_length=50)),
                ('detail_price', models.IntegerField()),
                ('detail_amount', models.IntegerField()),
                ('detail_unit', models.CharField(max_length=100)),
                ('detail_img', models.ImageField(upload_to='')),
                ('detail_goodsid', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('order_number', models.CharField(max_length=50)),
                ('order_addr', models.CharField(max_length=100)),
                ('order_recv', models.CharField(max_length=10)),
                ('order_fee', models.IntegerField(default=10)),
                ('order_status', models.SmallIntegerField(default=1, choices=[(1, '待付款'), (2, '待发货'), (3, '待收货'), (4, '已完成')])),
                ('order_pay', models.SmallIntegerField(default=1, choices=[(1, '货到付款'), (2, '微信支付'), (3, '支付宝支付'), (4, '银联支付')])),
                ('order_user', models.ForeignKey(to='users.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='goodsdetail',
            name='detail_goods',
            field=models.ForeignKey(to='order.Order'),
        ),
    ]
