from collections import OrderedDict
from rest_framework import serializers
from .models import Submission, Document, Result


class NonNullModelSerializer(serializers.ModelSerializer):
    """
    Removes null fields from response
    https://stackoverflow.com/questions/27015931/remove-null-fields-from-django-rest-framework-response
    Slightly modified for empty strings
    """

    def to_representation(self, instance):
        result = super(NonNullModelSerializer, self).to_representation(instance)
        return OrderedDict(
            [
                (key, result[key])
                for key in result
                if result[key] is not None and result[key] != ""
            ]
        )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ("id", "status")


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "name",
            "file",
            "submission",
            "text",
            "text_raw",
            "type",
            "language",
            "created_at",
            "updated_at",
        )


class ResultSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="match_id")
    name = serializers.CharField(source="match_name")

    class Meta:
        model = Result
        fields = ("id", "name", "percentage")


class DocumentDetailedSerializer(NonNullModelSerializer, serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ("id", "name", "total_percentage", "matches")

    def get_matches(self, obj):
        return obj.results.count()


class DocumentResultSerializer(serializers.ModelSerializer):
    matches = ResultSerializer(source="results", read_only=True, many=True)

    class Meta:
        model = Document
        fields = ("name", "text", "total_percentage", "matches", "ranges")
