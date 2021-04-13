from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("antiplag", "0011_add_and_fill_uuid_fields"),
    ]

    operations = [
        # Delete old ID fields
        migrations.RemoveField(model_name="document", name="id"),
        migrations.RemoveField(model_name="document", name="submission"),
        migrations.RemoveField(model_name="submission", name="id"),
        migrations.RemoveField(model_name="result", name="id"),
        migrations.RemoveField(model_name="result", name="document"),
    ]
