# Generated by Django 4.1.3 on 2022-12-05 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_comments_alter_listings_price_wishlist_auction_bids"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wishlist",
            name="item",
        ),
        migrations.AddField(
            model_name="wishlist",
            name="item",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="wishItem",
                to="auctions.listings",
            ),
        ),
    ]
