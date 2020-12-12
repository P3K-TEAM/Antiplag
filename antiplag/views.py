from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

from .serializers import SubmissionSerializer, DocumentSerializer
from .models import Submission, Document
from .constants import *


class FileList(APIView):
    def get(self, request, format=None):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileDetail(APIView):
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


class FileListMixin(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FileDetailMixin(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
