from django.test import TestCase

from ..enums import SubmissionStatus
from ..models import Submission, Document, Result


class ResultModelTestCase(TestCase):
    def setUp(self):
        self.submission = Submission.objects.create(status=SubmissionStatus.PROCESSED)
        self.document = Document.objects.create(
            name="document1",
            submission=self.submission,
            type=Document.DocumentType.TEXT,
        )

    def test_intervals(self):
        result1 = Result.objects.create(
            document=self.document,
            matched_docs=[
                {
                    "name": "A",
                    "percentage": 0.9,
                    "intervals": [
                        {
                            "fromA": 400,
                            "toA": 500,
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
                            "fromA": 5,
                            "toA": 9,
                        },
                        {
                            "fromA": 550,
                            "toA": 900,
                        },
                    ],
                },
                {
                    "name": "B",
                    "percentage": 0.15,
                    "intervals": [
                        {
                            "fromA": 17,
                            "toA": 27,
                        },
                    ],
                },
                {
                    "name": "C",
                    "percentage": 0.30,
                    "intervals": [
                        {
                            "fromA": 440,
                            "toA": 475,
                        },
                    ],
                },
            ],
        )

        expected = [
            {
                "ranges": {
                    "from": 0,
                    "to": 16,
                },
                "matches": [{"id": 0, "name": "A", "percentage": 0.9}],
            },
            {
                "ranges": {
                    "from": 17,
                    "to": 27,
                },
                "matches": [
                    {"id": 0, "name": "A", "percentage": 0.9},
                    {"id": 1, "name": "B", "percentage": 0.15},
                ],
            },
            {
                "ranges": {
                    "from": 28,
                    "to": 439,
                },
                "matches": [{"id": 0, "name": "A", "percentage": 0.9}],
            },
            {
                "ranges": {
                    "from": 440,
                    "to": 475,
                },
                "matches": [
                    {"id": 0, "name": "A", "percentage": 0.9},
                    {"id": 2, "name": "C", "percentage": 0.30},
                ],
            },
            {
                "ranges": {
                    "from": 476,
                    "to": 500,
                },
                "matches": [{"id": 0, "name": "A", "percentage": 0.9}],
            },
            {
                "ranges": {
                    "from": 550,
                    "to": 900,
                },
                "matches": [{"id": 0, "name": "A", "percentage": 0.9}],
            },
        ]

        self.assertListEqual(expected, result1.intervals)

    def test_empty_intervals(self):
        result1 = Result.objects.create(
            document=self.document,
            matched_docs=[],
        )

        expected = []

        self.assertListEqual(expected, result1.intervals)
