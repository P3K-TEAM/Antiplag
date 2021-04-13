import uuid
from functools import partial

from django.db import migrations, models


def migrate_to_uuid(apps, schema_editor, model, id_field, uuid_field):
    model_class = apps.get_model("antiplag", model)
    for model_instance in model_class.objects.all():
        obj_id = getattr(model_instance, id_field)
        if obj_id:
            print(obj_id)
            new_uuid = uuid.uuid5(uuid.NAMESPACE_OID, str(obj_id))
            setattr(model_instance, uuid_field, new_uuid)
            model_instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ("antiplag", "0010_submission_email"),
    ]

    operations = [
        # Add UUID fields
        migrations.AddField(
            model_name="document",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name="document",
            name="submission_uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name="submission",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name="result",
            name="document_uuid",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
        # Fill them up
        migrations.RunPython(
            partial(
                migrate_to_uuid, model="document", id_field="id", uuid_field="uuid"
            ),
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            partial(migrate_to_uuid, model="result", id_field="id", uuid_field="uuid"),
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            partial(
                migrate_to_uuid, model="submission", id_field="id", uuid_field="uuid"
            ),
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            partial(
                migrate_to_uuid,
                model="document",
                id_field="submission_id",
                uuid_field="submission_uuid",
            ),
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RunPython(
            partial(
                migrate_to_uuid,
                model="result",
                id_field="document_id",
                uuid_field="document_uuid",
            ),
            reverse_code=migrations.RunPython.noop,
        ),
    ]
