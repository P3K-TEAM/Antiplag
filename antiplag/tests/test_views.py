from django.test import TestCase

from ..models import Submission, Document, Result
from ..views import SubmissionGraphDetail


class GraphViewTestCase(TestCase):
    def setUp(self):
        self.submission = Submission.objects.create(
            status=Submission.SubmissionStatus.PROCESSED
        )
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
        Result.objects.create(
            document=self.document,
            matched_docs=[
                {"name": "test_name", "elastic_id": 123, "percentage": 0.19},
                {"name": "test_name2", "elastic_id": 1234, "percentage": 0.19},
            ],
        )
        Result.objects.create(
            document=self.document2,
            matched_docs=[
                {"name": "test_name", "elastic_id": 123, "percentage": 0.19},
                {"name": "test_name", "id": 1, "percentage": 0.19},
            ],
        )

        response = SubmissionGraphDetail().get(None, self.submission.id)
        result = response.data
        expected = {
            "nodes": [
                {"id": 1, "name": "whatever1", "uploaded": True},
                {"name": "test_name", "id": 123},
                {"name": "test_name2", "id": 1234},
                {"id": 2, "name": "whatever2", "uploaded": True},
            ],
            "links": [
                {"source": 1, "target": 123, "value": 0.19},
                {"source": 1, "target": 1234, "value": 0.19},
                {"source": 2, "target": 123, "value": 0.19},
                {"source": 2, "target": 1, "value": 0.19},
            ],
        }
        self.assertDictEqual(expected, result)

    def test_skip_missing_ids(self):
        Result.objects.create(
            document=self.document,
            matched_docs=[
                {"name": "test_name", "elastic_id": 123, "percentage": 0.19},
                {"name": "test_name2", "percentage": 0.19},
            ],
        )
        Result.objects.create(
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
                {"id": 3, "name": "whatever1", "uploaded": True},
                {"name": "test_name", "id": 123},
                {"id": 4, "name": "whatever2", "uploaded": True},
            ],
            "links": [{"source": 3, "target": 123, "value": 0.19}],
        }
        self.assertDictEqual(expected, result)
