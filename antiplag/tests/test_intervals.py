from django.test import TestCase

from ..enums import SubmissionStatus
from ..models import Submission, Document, Result


class ResultModelTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.submission = Submission.objects.create(status=SubmissionStatus.PROCESSED)
        self.document = Document.objects.create(
            name="document1",
            submission=self.submission,
            type=Document.DocumentType.TEXT,
        )

    def test_intervals(self):
        # result 1
        self.document.results.create(
            match_id="match-id-0",
            match_name="A",
            percentage=0.9,
            ranges=[
                {
                    "fromA": 5,
                    "toA": 9,
                },
                {
                    "fromA": 0,
                    "toA": 268,
                },
                {
                    "fromA": 268,
                    "toA": 440,
                },
                {
                    "fromA": 400,
                    "toA": 500,
                },
                {
                    "fromA": 550,
                    "toA": 900,
                },
            ],
        )

        # result 2
        self.document.results.create(
            match_id="match-id-1",
            match_name="B",
            percentage=0.15,
            ranges=[
                {
                    "fromA": 17,
                    "toA": 27,
                },
            ],
        )

        # result 3
        self.document.results.create(
            match_id="match-id-2",
            match_name="C",
            percentage=0.30,
            ranges=[
                {
                    "fromA": 440,
                    "toA": 475,
                },
            ],
        )

        expected = [
            {
                "from": 0,
                "to": 16,
                "matches": [{"id": "match-id-0", "name": "A", "percentage": 0.9}],
            },
            {
                "from": 17,
                "to": 27,
                "matches": [
                    {"id": "match-id-0", "name": "A", "percentage": 0.9},
                    {"id": "match-id-1", "name": "B", "percentage": 0.15},
                ],
            },
            {
                "from": 28,
                "to": 439,
                "matches": [{"id": "match-id-0", "name": "A", "percentage": 0.9}],
            },
            {
                "from": 440,
                "to": 475,
                "matches": [
                    {"id": "match-id-0", "name": "A", "percentage": 0.9},
                    {"id": "match-id-2", "name": "C", "percentage": 0.30},
                ],
            },
            {
                "from": 476,
                "to": 500,
                "matches": [{"id": "match-id-0", "name": "A", "percentage": 0.9}],
            },
            {
                "from": 550,
                "to": 900,
                "matches": [{"id": "match-id-0", "name": "A", "percentage": 0.9}],
            },
        ]

        self.assertListEqual(expected, self.document.ranges)


def test_empty_intervals(self):
    result = Result.objects.create(
        document=self.document,
        ranges=[],
    )

    expected = []

    self.assertListEqual(expected, result.intervals)
