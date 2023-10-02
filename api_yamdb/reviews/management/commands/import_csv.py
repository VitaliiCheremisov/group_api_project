import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, CustomUser, Genre, GenreTitle, Reviews, Title

FILES_CSV = {Category: 'category.csv',
             Comment: 'comments.csv',
             GenreTitle: 'genre_title.csv',
             Genre: 'genre.csv',
             Reviews: 'review.csv',
             Title: 'titles.csv',
             CustomUser: 'users.csv'
             }

class Command(BaseCommand):
    help = 'Загрузка данных из CSV файла в базу данных.'

    def handle(self, *args, **options):
        for model, file_csv in FILES_CSV.items:
            csv_file_path = f'{settings.BASE_DIR}/static/data/{file_csv}'

            with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                objects_to_create = []
                
                for row in csv_reader:
                    field_values = {
                        field: row.get(field.name) for field in model._meta.fields
                        }
                    objects_to_create.append(model(**field_values))
                model.objects.bulk_create(objects_to_create)

            self.stdout.write(self.style.SUCCESS(
                'Данные успешно загружены из CSV файла в базу данных'
                ))
