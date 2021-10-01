from rest_framework import serializers

from .models import Archive, Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'create_date', 'reg_number', 'comment']


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = ['id', 'name', 'create_date', 'doc_count']
