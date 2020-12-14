# Generated by Django 3.1.3 on 2020-12-12 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("antiplag", "0004_document_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="submission",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documents",
                to="antiplag.submission",
            ),
        ),
    ]
