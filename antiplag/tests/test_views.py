from django.test import TestCase

from ..enums import SubmissionStatus, MatchType
from ..models import Submission, Document
from ..views import SubmissionGraphDetail


class GraphViewTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
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
        # document 1
        self.document.results.create(
            match_type=MatchType.CORPUS,
            match_id=123,
            match_name="test_name",
            percentage=0.19,
            ranges=[],
        )
        self.document.results.create(
            match_type=MatchType.CORPUS,
            match_id=1234,
            match_name="test_name2",
            percentage=0.19,
            ranges=[],
        )

        # document 2
        self.document2.results.create(
            match_name="test_name2",
            match_type=MatchType.CORPUS,
            match_id=123,
            percentage=0.19,
            ranges=[],
        )
        self.document2.results.create(
            match_name="test_name2",
            match_type=MatchType.UPLOADED,
            match_id=str(self.document.id),
            percentage=0.19,
            ranges=[],
        )

        response = SubmissionGraphDetail().get(None, self.submission.id)
        result = response.data

        expected = {
            "nodes": [
                {"id": str(self.document.id), "name": "whatever1", "uploaded": True},
                {"id": "123", "name": "test_name"},
                {"id": "1234", "name": "test_name2"},
                {"id": str(self.document2.id), "name": "whatever2", "uploaded": True},
            ],
            "links": [
                {"source": str(self.document.id), "target": "123", "value": 0.19},
                {"source": str(self.document.id), "target": "1234", "value": 0.19},
                {"source": str(self.document2.id), "target": "123", "value": 0.19},
                {
                    "source": str(self.document2.id),
                    "target": str(self.document.id),
                    "value": 0.19,
                },
            ],
        }

        self.assertDictEqual(expected, result)
