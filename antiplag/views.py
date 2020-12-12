from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from . import serializers
from .models import Submission, Document
from .constants import *


class SubmissionList(APIView):
    serializer_class = serializers.SubmissionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):

        # TODO: Do not create save the submission to the DB unless all conditions are passing

        # create new submission
        submission = Submission.objects.create(
            status=Submission.SubmissionStatus.PENDING
        )

        # check for request content type
        is_file = CONTENT_TYPE_FILE in request.content_type
        is_text = CONTENT_TYPE_TEXT in request.content_type

        if not (is_file or is_text):
            return Response({'error': 'Unsupported Content-Type header'}, status=status.HTTP_400_BAD_REQUEST)

        if is_file:
            files = request.FILES.getlist("files")

            if not files:
                return Response({'error': 'No files present'}, status=status.HTTP_400_BAD_REQUEST)

            for file in files:
                Document.create_and_process_text(
                    submission=submission,
                    file=file
                )

        else:
            text_raw = request.body.decode()

            if not text_raw.strip():
                return Response({'error': 'No text was specified'}, status=status.HTTP_400_BAD_REQUEST)

            Document.create_and_process_text(
                submission=submission,
                text_raw=text_raw
            )

        return Response(self.serializer_class(submission).data, status=status.HTTP_201_CREATED)
