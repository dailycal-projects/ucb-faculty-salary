import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from salary.models import Person, DirectoryRecord


class Command(BaseCommand):
    help = "Export processed file of Berkeley faculty joined with department \
            information"

    def handle(self, *args, **options):
        processed_data_path = os.path.join(
            settings.DATA_DIR, 'processed_berkeley_faculty.csv')
        fieldnames = ['first', 'last', 'department', 'year',
                      'title_category', 'title', 'gross_salary']
        with open(processed_data_path, 'w') as processed_data_file:
            writer = csv.DictWriter(
                processed_data_file, fieldnames=fieldnames)
            writer.writeheader()
            for person in Person.objects.exclude(
                    directory_record__department_obj=None):
                row = {}
                row['first'] = person.first
                row['last'] = person.last
                row['department'] = person.directory_record.department_obj\
                    .canonical
                for salaryrecord in person.salaryrecord_set.all():
                    row['year'] = salaryrecord.year
                    row['title_category'] = salaryrecord.title_category
                    row['title'] = salaryrecord.title
                    row['gross_salary'] = salaryrecord.gross
                    writer.writerow(row)
