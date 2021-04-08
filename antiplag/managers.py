from math import ceil

from django.db import models

from antiplag.enums import SubmissionStatus


class SubmissionManager(models.Manager):
    def average_time(self):
        result = self.filter(status=SubmissionStatus.PROCESSED).aggregate(
            average_time=models.Avg(models.F("updated_at") - models.F("created_at"))
        )
        return ceil(result.get("average_time").seconds / 60)  # in minutes
