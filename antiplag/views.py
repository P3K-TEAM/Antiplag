from django.shortcuts import render
from .models import Submission, Document
from .serializers import SubmissionSerializer, DocumentSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView
import json
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

    def post(self, request, *args, **kwargs):
        submission_serializer = SubmissionSerializer(data={"status": Submission.SubmissionStatus.PENDING})
        if submission_serializer.is_valid():
            submission = submission_serializer.save()

            if CONTENT_TYPE_FILE in request.content_type:
                for file in request.FILES.getlist("files"):
                    document = Document.create_and_process_text(file=file)
                return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

            elif CONTENT_TYPE_TEXT in request.content_type:
                document = Document.create_and_process_text(submission=submission, text_raw=request.POST.get('text', "no_text_attribute"))
                return Response(SubmissionSerializer(submission).data, status=status.HTTP_200_OK)

            else:
                return Response( status=status.HTTP_400_BAD_REQUEST)



class FileLitsMixin(
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
