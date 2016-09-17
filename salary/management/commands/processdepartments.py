import os
import csv
from django.utils.text import slugify
from django.conf import settings
from django.core.management.base import BaseCommand
from salary.models import DirectoryRecord, Department


class Command(BaseCommand):
    help = "Add departmental information and create Department objects"

    def handle(self, *args, **options):
        Department.objects.all().delete()
        departments_path = os.path.join(settings.DATA_DIR, 'departments.csv')
        with open(departments_path, 'r') as departments_file:
            reader = csv.DictReader(departments_file)
            for row in reader:
                if row['keep'] == '0':
                    continue
                slug = slugify(row['canonical'])
                department, created = Department.objects.get_or_create(
                    slug=slug)
                department.canonical = row['canonical']
                department.discipline = row['discipline']
                code = row['code']
                if created:
                    department.codes = [code]
                else:
                    department.codes += [code]
                department.save()

        for record in DirectoryRecord.objects.all():
            try:
                code, desc = record.home_department.split('-')
                department = Department.objects.get(
                    codes__contains=[code.strip()])
                record.department_obj = department
                record.save()
            except:
                continue
