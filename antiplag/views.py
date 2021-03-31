from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from . import serializers
from .models import Submission, Document
from .constants import TEXT_SUBMISSION_NAME, CONTENT_TYPE_FILE, CONTENT_TYPE_JSON
from .tasks import process_documents

from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import json, requests


class SubmissionList(APIView):
    serializer_class = serializers.SubmissionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        submission = Submission(
            status=Submission.SubmissionStatus.PENDING,
        )

        # check for request content type
        is_file = CONTENT_TYPE_FILE in request.content_type
        is_text = CONTENT_TYPE_JSON in request.content_type

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
        if submission.status == Submission.SubmissionStatus.PROCESSED:
            data["documents"] = serializers.DocumentDetailedSerializer(
                submission.documents.all(), many=True
            ).data

        return Response(data=data)


class SubmissionGraphDetail(APIView):
    def get(self, request, id):
        submission = get_object_or_404(Submission, pk=id)

        nodes = {}
        links = []
        if submission.status == Submission.SubmissionStatus.PROCESSED:
            for doc in submission.documents.all():
                doc_data = serializers.DocumentDetailedSerializer(doc).data
                doc_id = doc_data["id"]
                nodes[doc_id] = {
                    "id": doc_id,
                    "name": doc_data["name"],
                    "uploaded": True,
                }

                matched_documents = doc.result.matched_docs
                for matched_doc in matched_documents:
                    # It's either elastic document or our document
                    matched_id = matched_doc.get("elastic_id", None) or matched_doc.get(
                        "id", None
                    )
                    if not matched_id:
                        continue

                    if matched_id not in nodes:
                        nodes[matched_id] = {
                            "name": matched_doc.get("name", ""),
                            "id": matched_id,
                        }

                    links.append(
                        {
                            "source": doc_id,
                            "target": matched_id,
                            "value": matched_doc.get("percentage", 0),
                        }
                    )
        return Response(data={"nodes": list(nodes.values()), "links": links})


class DocumentDetail(APIView):
    serializer_class = serializers.DocumentResultSerializer

    def get(self, request, id):
        document = get_object_or_404(Document, pk=id)

        if document.submission.status == Submission.SubmissionStatus.PROCESSED:
            return Response(
                {
                    "document": self.serializer_class(instance=document).data,
                    "submission_id": document.submission.id,
                    "is_multiple": document.submission.documents.count() > 1,
                }
            )
        else:
            # unprocessed submission documents should 'not exist' for the user
            return Response(status=status.HTTP_404_NOT_FOUND)


class DocumentDiff(APIView):
    def get(self, request, first_id, second_id):
        first_document = get_object_or_404(Document, pk=first_id)
        second_document = None
        intervals = []

        if first_document.submission.status == Submission.SubmissionStatus.PROCESSED:

            second_document = next(
                doc
                for doc in first_document.result.matched_docs
                if doc["elastic_id"] == second_id
            )

            if not second_document:
                return Response(status=status.HTTP_404_NOT_FOUND)

            intervals = second_document["intervals"]

            return Response(
                {
                    "textA": {
                        "name": first_document.name,
                        "content": first_document.text,
                    },
                    "textB": {
                        "name": second_document["name"],
                        "content": second_document["text"],
                    },
                    "matches": intervals,
                }
            )
        else:
            # unprocessed submission documents should 'not exist' for the user
            return Response(status=status.HTTP_404_NOT_FOUND)
