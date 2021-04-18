import uuid

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from . import serializers
from .enums import SubmissionStatus, MatchType
from .models import Submission, Document
from .constants import (
    TEXT_SUBMISSION_NAME,
    FILE_UPLOAD_CONTENT_TYPE,
    TEXT_UPLOAD_CONTENT_TYPE,
)
from .tasks import process_documents
from nlp.elastic import Elastic

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json


class Stats(APIView):
    @method_decorator(cache_page(60 * 60))
    def get(self, request):
        return Response(
            data={
                "submission_count": Submission.objects.count(),
                "submission_avg_time": Submission.objects.average_time(),
                "corpus_size": Elastic.count(),
            }
        )


class SubmissionList(APIView):
    serializer_class = serializers.SubmissionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        submission = Submission(status=SubmissionStatus.PENDING)

        # check for request content type
        is_file = FILE_UPLOAD_CONTENT_TYPE in request.content_type
        is_text = TEXT_UPLOAD_CONTENT_TYPE in request.content_type

        if not (is_file or is_text):
            return Response(
                {"error": _("Unsupported Content-Type header.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if is_file:
            files = request.FILES.getlist("files")

            if len(files) > settings.MAX_FILES_PER_REQUEST:
                return Response(
                    {
                        "error": _(
                            "More than max allowed files per request submitted. (%s)"
                        )
                        % settings.MAX_FILES_PER_REQUEST
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not files:
                return Response(
                    {"error": _("No files present.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request_contains_large_file = next(
                (
                    file
                    for file in files
                    if file.size > settings.MAX_FILE_SIZE * 1024 * 1024
                ),
                False,
            )

            if request_contains_large_file != False:
                return Response(
                    {
                        "error": _("Maximum filesize exceeded. (%s) MB")
                        % settings.MAX_FILE_SIZE
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = request.POST.get("email", None)
            if email is not None:
                try:
                    validate_email(email)
                except ValidationError as e:
                    return Response(
                        {"error": _("Unrecognized email address format.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            submission.email = email
            submission.save()

            for file in files:
                Document.objects.create(
                    file=file,
                    name=file.name,
                    submission=submission,
                    type=Document.DocumentType.FILE,
                )

        else:
            data = json.loads(request.body)
            text_raw = data["text"]
            email = data["email"] if "email" in data else None

            if not text_raw.strip():
                return Response(
                    {"error": _("No text was specified.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if email is not None:
                try:
                    validate_email(email)
                except ValidationError as e:
                    return Response(
                        {"error": _("Unrecognized email address format.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            submission.email = email
            submission.save()

            Document.objects.create(
                name=TEXT_SUBMISSION_NAME,
                submission=submission,
                type=Document.DocumentType.TEXT,
                text_raw=text_raw,
            )
        # Run background task that processes documents
        process_documents.delay(submission.id)

        return Response(
            self.serializer_class(submission).data, status=status.HTTP_201_CREATED
        )


class SubmissionDetail(APIView):
    serializer_class = serializers.SubmissionSerializer

    def get(self, request, id):
        submission = get_object_or_404(Submission, pk=id)

        data = {
            **self.serializer_class(instance=submission).data,
        }

        # in case the submission is processed, include the documents
        if submission.status == SubmissionStatus.PROCESSED:
            data["documents"] = serializers.DocumentDetailedSerializer(
                submission.documents.all(), many=True
            ).data

        return Response(data=data)


class SubmissionGraphDetail(APIView):
    def get(self, request, id):
        submission = get_object_or_404(Submission, pk=id)

        nodes = {}
        links = []

        if submission.status == SubmissionStatus.PROCESSED:
            for doc in submission.documents.all():

                nodes[doc.id] = {
                    "id": str(doc.id),
                    "name": doc.name,
                    "uploaded": True,
                }

                for result in doc.results.all():

                    if result.match_type == MatchType.UPLOADED:
                        # internal uuid
                        match_id = uuid.UUID(result.match_id)
                    else:
                        # elastic id
                        match_id = result.match_id

                    if match_id not in nodes:
                        nodes[match_id] = {
                            "id": str(match_id),
                            "name": result.match_name,
                        }

                    links.append(
                        {
                            "source": str(doc.id),
                            "target": str(match_id),
                            "value": result.percentage,
                        }
                    )

        return Response(data={"nodes": list(nodes.values()), "links": links})


class DocumentDetail(APIView):
    serializer_class = serializers.DocumentResultSerializer

    def get(self, request, id):
        document = get_object_or_404(Document, pk=id)

        if document.submission.status == SubmissionStatus.PROCESSED:
            return Response(
                {
                    "document": self.serializer_class(instance=document).data,
                    "submission_id": document.submission.id,
                }
            )
        else:
            # unprocessed submission documents should 'not exist' for the user
            return Response(status=status.HTTP_404_NOT_FOUND)


class DocumentDiff(APIView):
    def get(self, request, first_id, second_id):
        first_document = get_object_or_404(Document, pk=first_id)

        if first_document.submission.status == SubmissionStatus.PROCESSED:

            # find document to compare with
            second_document_result = next(
                (
                    result
                    for result in first_document.results.all()
                    if result.match_id == second_id
                ),
                None,
            )
            print(second_document_result)
            if not second_document_result:
                return Response(status=status.HTTP_404_NOT_FOUND)

            # get second document content (internal or elastic)
            if second_document_result.match_type == MatchType.UPLOADED:
                second_document_content = Document.objects.get(pk=second_id).text
            else:
                second_document_content = Elastic.get(id=second_id)["text_preprocessed"]

            return Response(
                {
                    "textA": {
                        "name": first_document.name,
                        "content": first_document.text,
                    },
                    "textB": {
                        "name": second_document_result.match_name,
                        "content": second_document_content,
                    },
                    "ranges": second_document_result.ranges,
                }
            )
        else:
            # unprocessed submission documents should 'not exist' for the user
            return Response(status=status.HTTP_404_NOT_FOUND)
