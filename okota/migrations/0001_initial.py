# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryFee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.FloatField(null=True, blank=True)),
                ('eta', models.IntegerField(default=1)),
                ('delivery_type', models.CharField(default=b'Courier', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeliveryPersonnel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivery_fee', models.ManyToManyField(to='okota.DeliveryFee', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LocationDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, null=True, blank=True)),
                ('street', models.CharField(max_length=100, null=True, blank=True)),
                ('suburb', models.CharField(max_length=100, null=True, blank=True)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('province', models.CharField(max_length=100, null=True, blank=True)),
                ('country', models.CharField(max_length=100, null=True, blank=True)),
                ('latitude', models.CharField(max_length=100, null=True, blank=True)),
                ('longitude', models.CharField(max_length=100, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session', models.CharField(max_length=500, null=True, blank=True)),
                ('contact_person', models.CharField(max_length=100, null=True, blank=True)),
                ('status', models.CharField(max_length=100, null=True, blank=True)),
                ('datetime_stamp', models.DateTimeField(null=True, blank=True)),
                ('payment_method', models.CharField(max_length=100, null=True, blank=True)),
                ('checked_out', models.BooleanField(default=False)),
                ('final_amount', models.FloatField(default=0, null=True, blank=True)),
                ('contact_number', models.ForeignKey(blank=True, to='okota.ContactDetail', null=True)),
                ('delivery_address', models.ForeignKey(blank=True, to='okota.LocationDetail', null=True)),
                ('delivery_person', models.ForeignKey(blank=True, to='okota.DeliveryPersonnel', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProductAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductIngredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reviewers_name', models.CharField(max_length=100)),
                ('review', models.CharField(max_length=500)),
                ('rating', models.FloatField(default=0)),
                ('stamp', models.DateTimeField(auto_now=True)),
                ('is_moderated', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RetailStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('contact', models.ManyToManyField(to='okota.ContactDetail', null=True, blank=True)),
                ('location', models.ForeignKey(blank=True, to='okota.LocationDetail', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StoreProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField(null=True, blank=True)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('picture', models.ImageField(default=b'products_pictures/okota-image-unavailable.png', null=True, upload_to=b'products_pictures', blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('ingredients', models.ManyToManyField(to='okota.ProductIngredient', null=True, blank=True)),
                ('reviews', models.ManyToManyField(to='okota.ProductReview', null=True, blank=True)),
                ('store', models.ForeignKey(related_name=b'ProductStore', to='okota.RetailStore')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reviewers_name', models.CharField(max_length=100)),
                ('review', models.CharField(max_length=500)),
                ('stamp', models.DateTimeField(auto_now=True)),
                ('is_moderated', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True, verbose_name='gender', choices=[(b'Male', b'Male'), (b'Female', b'Female')])),
                ('contacts', models.ManyToManyField(to='okota.ContactDetail', null=True, blank=True)),
                ('locations', models.ManyToManyField(to='okota.LocationDetail', null=True, blank=True)),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='retailstore',
            name='profile',
            field=models.ForeignKey(related_name=b'StoreProfile', to='okota.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='attributes',
            field=models.ManyToManyField(to='okota.OrderProductAttribute', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='delivery_fee',
            field=models.ForeignKey(blank=True, to='okota.DeliveryFee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(to='okota.StoreProduct'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='okota.OrderProduct', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliverypersonnel',
            name='profile',
            field=models.OneToOneField(to='okota.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='location',
            field=models.ForeignKey(to='okota.LocationDetail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deliveryfee',
            name='store',
            field=models.ForeignKey(to='okota.RetailStore'),
            preserve_default=True,
        ),
    ]
