# Generated by Django 5.0.6 on 2024-06-11 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chain_gpt", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vectordata",
            name="data",
        ),
        migrations.RemoveField(
            model_name="vectordata",
            name="vector",
        ),
        migrations.AddField(
            model_name="vectordata",
            name="answer",
            field=models.TextField(default="default_answer"),
        ),
        migrations.AddField(
            model_name="vectordata",
            name="category",
            field=models.CharField(default="default_category", max_length=255),
        ),
        migrations.AddField(
            model_name="vectordata",
            name="embedding",
            field=models.BinaryField(default=b""),
        ),
        migrations.AddField(
            model_name="vectordata",
            name="question",
            field=models.TextField(default="default_question"),
        ),
    ]
