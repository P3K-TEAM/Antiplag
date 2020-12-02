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
from langdetect import detect


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

            if request.META['HTTP_TYPE'] == Document.DocumentType.FILE:
                for file in request.FILES.getlist("files"):
                    text = Document.process_file(self, file)
                    text_raw = Document.process_raw_text(self, text)
                    language = Document.detect_language(self, text_raw)
                    doc_serializer = DocumentSerializer(data={"file": file,
                                                              "type": Document.DocumentType.FILE,
                                                              "text": text,
                                                              "text_raw": text_raw,
                                                              "language": language
                                                              })
                    if doc_serializer.is_valid():
                        document = doc_serializer.save()
                        document.submission = submission
                        document.save()
                return Response(SubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)
            elif request.META['HTTP_TYPE'] == Document.DocumentType.TEXT:

                text = request.POST.get('text', "no_text_attribute")
                raw_text = request.POST.get('text', "no_text_attribute")
                language = Document.detect_language(self, raw_text)
                doc_serializer = DocumentSerializer(data={"type": Document.DocumentType.FILE,
                                                          "text": text,
                                                          "text_raw": raw_text,
                                                          "language": language
                                                          })
                if doc_serializer.is_valid():
                    document = doc_serializer.save()
                    document.submission = submission
                    document.save()
                else:
                    print(doc_serializer.errors)
                return Response(doc_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        document = self.get_object(pk)
        serializer = DocumentSerializer(document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        document = self.get_object(pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
