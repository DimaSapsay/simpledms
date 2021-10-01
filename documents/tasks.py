import pandas as pd
import pathlib
import zipfile
from celery import shared_task

from .models import Document


def create_xlsx_file(documents, register_name):
    columns = ['Реєстраційний номер', 'Дата створення', 'Короткий опис', 'Посилання на файл']

    df = pd.DataFrame(documents)

    writer = pd.ExcelWriter(f'media/{register_name}',
                            engine='xlsxwriter',
                            date_format='dd.mm.yyyy')

    df.to_excel(writer, sheet_name='Sheet1', header=columns, index=False)

    worksheet = writer.sheets['Sheet1']
    worksheet.set_column('A:A', 22)
    worksheet.set_column('B:B', 18)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 25)

    writer.save()


def create_zip_file(documents, register_name, zip_name):
    zip_file = zipfile.ZipFile(f'media/archive/{zip_name}.zip', 'w')

    zip_file.write(f'media/{register_name}', register_name)

    for document in documents:
        file_name = document['main_file'].replace('document/', '')
        zip_file.write(
            f'media/{document["main_file"]}',
            f'Документи/{document["reg_number"]}/{file_name}'
        )

    pathlib.Path(f'media/{register_name}').unlink(missing_ok=True)


@shared_task
def create_archive(start, end, zip_name):

    register_name = 'Реєстр документів.xlsx'

    documents = (
        Document.objects
            .filter(create_date__range=(start, end))
            .values('reg_number', 'create_date', 'comment', 'main_file')
            .order_by('create_date')
    )

    create_xlsx_file(documents, register_name)

    create_zip_file(documents, register_name, zip_name)
