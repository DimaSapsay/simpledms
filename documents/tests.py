import pathlib
from datetime import date, timedelta

from django.core.files import File
from django.test import TestCase, Client
from rest_framework import status

from .models import Archive, Document
from .serializers import ArchiveSerializer, DocumentSerializer


client = Client()


class GetAllDocumentsTest(TestCase):

    def setUp(self):
        for number in range(4):
            with open(f'simple_{number}.txt', 'w') as f:
                f.write('Some text')

            Document.objects.create(
                title=f'Документ №{number}',
                main_file=File(open(f'simple_{number}.txt', 'rb')),
                reg_number=f'000-00{number}',
                comment=f'Коментар {number}'
            )

    def tearDown(self):
        for number in range(4):
            pathlib.Path(f'simple_{number}.txt').unlink(missing_ok=True)
            pathlib.Path(f'media/document/simple_{number}.txt').unlink(missing_ok=True)

    def test_get_all_documents(self):
        response = client.get('/doc/')
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleDocumentTest(TestCase):

    def setUp(self):
        with open('simple_1.txt', 'w') as f:
            f.write('Some text 1')

        Document.objects.create(
            title='Документ №1',
            main_file=File(open('simple_1.txt', 'rb')),
            reg_number='000-001',
            comment='Коментар 1'
        )

        with open('simple_2.txt', 'w') as f:
            f.write('Some text 2')

        self.document = Document.objects.create(
            title='Документ №2',
            main_file=File(open('simple_2.txt', 'rb')),
            reg_number='000-002',
            comment='Коментар 2'
        )

    def tearDown(self):
        pathlib.Path('simple_1.txt').unlink(missing_ok=True)
        pathlib.Path('media/document/simple_1.txt').unlink(missing_ok=True)
        pathlib.Path('simple_2.txt').unlink(missing_ok=True)
        pathlib.Path('media/document/simple_2.txt').unlink(missing_ok=True)

    def test_get_valid_single_document(self):
        response = client.get(f'/doc/{self.document.pk}/')
        document = Document.objects.get(pk=self.document.pk)
        serializer = DocumentSerializer(document)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_document(self):
        response = client.get(f'/doc/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewDocumentTest(TestCase):

    def setUp(self):
        with open('simple_1.txt', 'w') as f:
            f.write('Some text 1')

        self.payload = dict(
            title='Документ №1',
            main_file=File(open('simple_1.txt', 'rb')),
            reg_number='000-001',
            comment='Коментар 1'
        )

    def tearDown(self):
        pathlib.Path('simple_1.txt').unlink(missing_ok=True)
        pathlib.Path('media/document/simple_1.txt').unlink(missing_ok=True)

    def test_create_document(self):
        response = client.post('/doc/', data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UpdateSingleDocumentTest(TestCase):

    def setUp(self):
        with open('simple_1.txt', 'w') as f:
            f.write('Some text 1')

        self.document = Document.objects.create(
            title='Документ №1',
            main_file=File(open('simple_1.txt', 'rb')),
            reg_number='000-001',
            comment='Коментар 1'
        )

        self.payload = dict(
            title='Документ №100',
            reg_number='111-111',
            comment='Коментар 100'
        )

    def tearDown(self):
        pathlib.Path('simple_1.txt').unlink(missing_ok=True)
        pathlib.Path('media/document/simple_1.txt').unlink(missing_ok=True)

    def test_valid_update_document(self):
        response = client.put(f'/doc/{self.document.pk}/', **self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_found_update_document(self):
        response = client.put(f'/doc/30/', **self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteSingleDocumentTest(TestCase):

    def setUp(self):
        with open('simple_1.txt', 'w') as f:
            f.write('Some text 1')

        self.document = Document.objects.create(
            title='Документ №1',
            main_file=File(open('simple_1.txt', 'rb')),
            reg_number='000-001',
            comment='Коментар 1'
        )

    def tearDown(self):
        pathlib.Path('simple_1.txt').unlink(missing_ok=True)
        pathlib.Path('media/document/simple_1.txt').unlink(missing_ok=True)

    def test_valid_delete_document(self):
        response = client.delete(f'/doc/{self.document.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_document(self):
        response = client.delete(f'/doc/30/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllArchivesTest(TestCase):

    def setUp(self):
        for number in range(4):
            with open(f'zipfile_{number}', 'w') as f:
                f.write('Some text')

            Archive.objects.create(
                name=f'Архів №{number}',
                doc_count=4,
                zip_file=File(open(f'zipfile_{number}', 'rb')),
            )

    def tearDown(self):
        for number in range(4):
            pathlib.Path(f'zipfile_{number}').unlink(missing_ok=True)
            pathlib.Path(f'media/archive/zipfile_{number}').unlink(missing_ok=True)

    def test_get_all_archives(self):
        response = client.get('/doc/archive/')
        archives = Archive.objects.all()
        serializer = ArchiveSerializer(archives, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleArchiveTest(TestCase):

    def setUp(self):
        with open('zipfile_1', 'w') as f:
            f.write('Some text 1')

        Archive.objects.create(
            name='Архів №1',
            doc_count=4,
            zip_file=File(open('zipfile_1', 'rb')),
        )

        with open('zipfile_2', 'w') as f:
            f.write('Some text 1')

        self.archive = Archive.objects.create(
            name='Архів №2',
            doc_count=4,
            zip_file=File(open('zipfile_2', 'rb')),
        )

    def tearDown(self):
        pathlib.Path('zipfile_1').unlink(missing_ok=True)
        pathlib.Path('zipfile_2').unlink(missing_ok=True)
        pathlib.Path('media/archive/zipfile_1').unlink(missing_ok=True)
        pathlib.Path('media/archive/zipfile_2').unlink(missing_ok=True)

    def test_get_valid_single_archive(self):
        response = client.get(f'/doc/archive/{self.archive.pk}/')
        archive = Archive.objects.get(pk=self.archive.pk)
        serializer = ArchiveSerializer(archive)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_archive(self):
        response = client.get(f'/doc/archive/100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetDocumentsByPeriodTest(TestCase):
    def setUp(self):
        for number in range(4):
            with open(f'simple_{number}.txt', 'w') as f:
                f.write('Some text')

            Document.objects.create(
                title=f'Документ №{number}',
                main_file=File(open(f'simple_{number}.txt', 'rb')),
                reg_number=f'000-00{number}',
                comment=f'Коментар {number}'
            )

    def tearDown(self):
        for number in range(4):
            pathlib.Path(f'simple_{number}.txt').unlink(missing_ok=True)
            pathlib.Path(f'media/document/simple_{number}.txt').unlink(missing_ok=True)

    def test_create_archive(self):

        now = date.today().strftime('%Y-%m-%d')
        start = date.today() - timedelta(days=1)
        end = date.today() + timedelta(days=1)

        response = client.get(f'/doc/period/{start}/{end}/')
        documents = Document.objects.filter(create_date__range=(start, end))
        archive = Archive.objects.get(create_date=now)
        serializer = ArchiveSerializer(archive)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data['doc_count'], documents.count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_data_for_period(self):

        start = date.today() - timedelta(days=10)
        end = date.today() - timedelta(days=1)

        response = client.get(f'/doc/period/{start}/{end}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_no_logic_in_dates(self):

        start = date.today() + timedelta(days=100)
        end = date.today() - timedelta(days=100)

        response = client.get(f'/doc/period/{start}/{end}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_dates_format(self):
        response = client.get(f'/doc/period/2021-08-01/2021-08-99/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
