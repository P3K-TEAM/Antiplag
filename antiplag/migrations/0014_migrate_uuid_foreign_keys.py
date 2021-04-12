from django.db import migrations, models


def populate_submission_fk(apps, schema_editor):
    Document = apps.get_model("antiplag", "Document")
    for document in Document.objects.all():
        document.submission_id = document.submission_uuid
        document.save()


def populate_document_fk(apps, schema_editor):
    Result = apps.get_model("antiplag", "Result")
    for result in Result.objects.all():
        result.document_id = result.document_uuid
        result.save()


class Migration(migrations.Migration):
    dependencies = [
        ("antiplag", "0013_make_uuid_fields_pk"),
    ]

    operations = [
        migrations.AddField(
            model_name="Document",
            name="submission",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                null=True,
                related_name="documents",
                to="antiplag.Submission",
            ),
        ),
        migrations.AddField(
            model_name="Result",
            name="document",
            field=models.OneToOneField(
                on_delete=models.CASCADE,
                null=True,
                related_name="result",
                to="antiplag.Document",
            ),
        ),
        # Fill submission with submission_uuid data
        migrations.RunPython(populate_submission_fk, migrations.RunPython.noop),
        migrations.RunPython(populate_document_fk, migrations.RunPython.noop),
        # Remove submission_uuid and document_uuid
        migrations.RemoveField(model_name="Document", name="submission_uuid"),
        migrations.RemoveField(model_name="Result", name="document_uuid"),
    ]
