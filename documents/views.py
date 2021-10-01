import random
import string
from datetime import datetime

from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Archive, Document
from .serializers import ArchiveSerializer, DocumentSerializer
from .tasks import create_archive


class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = MultiPartParser,


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = MultiPartParser,


class DocumentPeriodList(APIView):

    def get(self, request, start, end):

        try:
            start = datetime.strptime(start, '%Y-%m-%d')
            end = datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if start > end:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        doc_count = Document.objects.filter(create_date__range=(start, end)).count()

        if not doc_count:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # random zip_name
        zip_name = f"{datetime.now().strftime('%d-%m-%Y')}-" \
                   f"{''.join(random.choice(string.ascii_letters) for _ in range(4))}"

        create_archive.delay(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), zip_name)

        archive = Archive.objects.create(
            name=zip_name,
            doc_count=doc_count,
            zip_file=f"archive/{zip_name}.zip"
        )

        serializer = ArchiveSerializer(archive)

        return Response(serializer.data)


class ArchiveList(generics.ListAPIView):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer


class ArchiveDetail(generics.RetrieveAPIView):
    queryset = Archive.objects.all()
    serializer_class = ArchiveSerializer
