# Generated by Django 4.1.3 on 2022-12-05 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0005_comments_comment_comments_commenter_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comments",
            name="time",
            field=models.TimeField(default=None),
        ),
    ]
