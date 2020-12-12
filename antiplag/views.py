from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .serializers import SubmissionSerializer
from .models import Submission, Document
from .constants import *


class SubmissionList(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        submission_serializer = SubmissionSerializer(data={"status": Submission.SubmissionStatus.PENDING})

        if submission_serializer.is_valid():
            submission = submission_serializer.save()

            is_file = CONTENT_TYPE_FILE in request.content_type
            is_text = CONTENT_TYPE_TEXT in request.content_type

            if not (is_file or is_text):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if is_file:
                for file in request.FILES.getlist("files"):
                    Document.create_and_process_text(
                        submission=submission,
                        file=file
                    )

            else:
                Document.create_and_process_text(
                    submission=submission,
                    text_raw=request.body.decode()
                )

            return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)
