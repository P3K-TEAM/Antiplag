from django.test import TestCase

from ..enums import SubmissionStatus
from ..models import Submission, Document, Result
from ..views import SubmissionGraphDetail


class GraphViewTestCase(TestCase):
    def setUp(self):
        self.submission = Submission.objects.create(status=SubmissionStatus.PROCESSED)
        self.document = Document.objects.create(
            name="whatever1",
            submission=self.submission,
            type=Document.DocumentType.TEXT,
        )
        self.document2 = Document.objects.create(
            name="whatever2",
            submission=self.submission,
            type=Document.DocumentType.TEXT,
        )

    def test_handle_duplicates(self):
        result1 = Result.objects.create(
            document=self.document,
            matched_docs=[
                {"name": "test_name", "elastic_id": 123, "percentage": 0.19},
                {"name": "test_name2", "elastic_id": 1234, "percentage": 0.19},
            ],
        )
        result2 = Result.objects.create(
            document=self.document2,
            matched_docs=[
                {"name": "test_name", "elastic_id": 123, "percentage": 0.19},
                {"name": "test_name", "id": str(self.document.id), "percentage": 0.19},
            ],
        )

        response = SubmissionGraphDetail().get(None, self.submission.id)
        result = response.data
        expected = {
            "nodes": [
                {"id": str(self.document.id), "name": "whatever1", "uploaded": True},
                {"name": "test_name", "id": 123},
                {"name": "test_name2", "id": 1234},
                {"id": str(self.document2.id), "name": "whatever2", "uploaded": True},
            ],
            "links": [
                {"source": str(self.document.id), "target": 123, "value": 0.19},
                {"source": str(self.document.id), "target": 1234, "value": 0.19},
                {"source": str(self.document2.id), "target": 123, "value": 0.19},
                {
                    "source": str(self.document2.id),
                    "target": str(self.document.id),
                    "value": 0.19,
                },
            ],
        }
        self.assertDictEqual(expected, result)

    def test_skip_missing_ids(self):
        result1 = Result.objects.create(
            document=self.document,
            matched_docs=[
                {"name": "test_name", "elastic_id": 123, "percentage": 0.19},
                {"name": "test_name2", "percentage": 0.19},
            ],
        )
        result2 = Result.objects.create(
            document=self.document2,
            matched_docs=[
                {"name": "test_name", "percentage": 0.19},
                {"name": "test_name", "percentage": 0.19},
            ],
        )

        response = SubmissionGraphDetail().get(None, self.submission.id)
        result = response.data
        expected = {
            "nodes": [
                {"id": str(self.document.id), "name": "whatever1", "uploaded": True},
                {"name": "test_name", "id": 123},
                {"id": str(self.document2.id), "name": "whatever2", "uploaded": True},
            ],
            "links": [{"source": str(self.document.id), "target": 123, "value": 0.19}],
        }
        self.assertDictEqual(expected, result)
