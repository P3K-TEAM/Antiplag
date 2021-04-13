from django.db import migrations, models
import antiplag.encoders


def populate_submission_fk(apps, schema_editor):
    Document = apps.get_model("antiplag", "document")
    for document in Document.objects.all():
        document.submission_id = document.submission_uuid
        document.save()


def populate_document_fk(apps, schema_editor):
    Result = apps.get_model("antiplag", "result")
    for result in Result.objects.all():
        result.document_id = result.document_uuid
        result.save()


class Migration(migrations.Migration):
    dependencies = [
        ("antiplag", "0013_make_uuid_fields_pk"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="submission",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                null=True,
                related_name="documents",
                to="antiplag.submission",
            ),
        ),
        migrations.AddField(
            model_name="result",
            name="document",
            field=models.OneToOneField(
                on_delete=models.CASCADE,
                null=True,
                related_name="result",
                to="antiplag.document",
            ),
        ),
        # Fill submission with submission_uuid data
        migrations.RunPython(populate_submission_fk, migrations.RunPython.noop),
        migrations.RunPython(populate_document_fk, migrations.RunPython.noop),
        # Remove submission_uuid and document_uuid
        migrations.RemoveField(model_name="document", name="submission_uuid"),
        migrations.RemoveField(model_name="result", name="document_uuid"),
        migrations.AlterField(
            model_name="result",
            name="document",
            field=models.OneToOneField(
                on_delete=models.CASCADE,
                null=False,
                related_name="result",
                to="antiplag.document",
            ),
        ),
        migrations.AlterField(
            model_name="result",
            name="matched_docs",
            field=models.JSONField(encoder=antiplag.encoders.UUIDEncoder),
        ),
    ]
