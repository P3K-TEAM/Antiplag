import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("antiplag", "0012_delete_old_primary_keys"),
    ]

    operations = [
        # Rename PKs
        migrations.RenameField(model_name="document", old_name="uuid", new_name="id"),
        migrations.RenameField(model_name="submission", old_name="uuid", new_name="id"),
        migrations.RenameField(model_name="result", old_name="uuid", new_name="id"),
        # Make UUID fields unique and PK
        migrations.AlterField(
            model_name="document",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                null=False,
            ),
        ),
        migrations.AlterField(
            model_name="submission",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                null=False,
            ),
        ),
        migrations.AlterField(
            model_name="result",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                null=False,
            ),
        ),
    ]
