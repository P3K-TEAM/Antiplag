from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("antiplag", "0011_add_and_fill_uuid_fields"),
    ]

    operations = [
        # Delete old ID fields
        migrations.RemoveField(model_name="Document", name="id"),
        migrations.RemoveField(model_name="Document", name="submission"),
        migrations.RemoveField(model_name="Submission", name="id"),
        migrations.RemoveField(model_name="Result", name="id"),
        migrations.RemoveField(model_name="Result", name="document"),
    ]
