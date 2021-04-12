import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("antiplag", "0012_delete_old_primary_keys"),
    ]

    operations = [
        # Rename PKs
        migrations.RenameField(model_name="Document", old_name="uuid", new_name="id"),
        migrations.RenameField(model_name="Submission", old_name="uuid", new_name="id"),
        migrations.RenameField(model_name="Result", old_name="uuid", new_name="id"),
        # Make UUID fields unique and PK
        migrations.AlterField(
            model_name="Document",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="Submission",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="Result",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
