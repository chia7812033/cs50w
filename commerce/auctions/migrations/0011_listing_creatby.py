# Generated by Django 4.1 on 2022-11-23 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_bid_rename_item_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='creatby',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
